import hashlib
import json
import logging
import operator
import posixpath
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from functools import reduce
from itertools import groupby
from random import getrandbits
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import sqlalchemy as sa
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
    UniqueConstraint,
    and_,
    select,
)
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import true

from dql.dataset import DATASET_CORE_COLUMN_NAMES, DatasetRecord, DatasetRow
from dql.dataset import Status as DatasetStatus
from dql.error import DatasetNotFoundError, StorageNotFoundError
from dql.node import AnyNode, DirType, Node, NodeWithPath
from dql.storage import Status as StorageStatus
from dql.storage import Storage
from dql.utils import GLOB_CHARS, is_expired

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.schema import SchemaItem

    from dql.data_storage import schema

logger = logging.getLogger("dql")

RANDOM_BITS = 63  # size of the random integer field


class AbstractDataStorage(ABC):
    """
    Abstract Data Storage class, to be implemented by any Database Adapters
    for a specific database system. This manages the storing, searching, and
    retrieval of indexed metadata, and has shared logic for all database
    systems currently in use.
    """

    #
    # Constants, Initialization, and Tables
    #

    LISTING_TABLE_NAME_PREFIX = "dsrc_"
    DATASET_TABLE_PREFIX = "ds_"
    TABLE_NAME_SHA_LIMIT = 12
    STORAGE_TABLE = "buckets"
    DATASET_TABLE = "datasets"
    DATASET_VERSION_TABLE = "datasets_versions"

    metadata: "MetaData"
    engine: "Engine"
    schema: "schema.Schema"

    storage_class = Storage
    dataset_class = DatasetRecord
    glob_op = "GLOB"

    def __init__(self, uri: str = ""):
        self.metadata = MetaData()
        self.uri = uri.rstrip("/")
        self._table: Optional[Table] = None
        self._nodes: Optional["schema.Node"] = None
        self._storages: Optional[Table] = None
        self._partials: Optional[Table] = None
        self._datasets: Optional[Table] = None
        self._datasets_versions: Optional[Table] = None
        self.dataset_fields = [
            c.name for c in self.datasets_columns() if c.name  # type: ignore[attr-defined] # noqa: E501
        ]
        self.node_fields = [c.name for c in self.schema.node_cls.default_columns()]
        self.path_str_index = self.node_fields.index("path_str")

    @staticmethod
    def buckets_columns() -> List["SchemaItem"]:
        return [
            Column("id", Integer, primary_key=True, nullable=False),
            Column("uri", Text, nullable=False),
            Column("timestamp", DateTime),
            Column("expires", DateTime),
            Column("started_inserting_at", DateTime),
            Column("last_inserted_at", DateTime),
            Column("status", Integer, nullable=False),
            Column("symlinks", Boolean, nullable=False),
        ]

    @staticmethod
    def datasets_columns() -> List["SchemaItem"]:
        return [
            Column("id", Integer, primary_key=True),
            Column("name", Text, nullable=False),
            Column("description", Text),
            Column("labels", JSON, nullable=True),
            Column("shadow", Boolean, nullable=False),
            Column("status", Integer, nullable=False),
            Column("created_at", DateTime),
            Column("finished_at", DateTime),
        ]

    @staticmethod
    def datasets_versions_columns() -> List["SchemaItem"]:
        return [
            Column("id", Integer, primary_key=True),
            Column(
                "dataset_id",
                Integer,
                ForeignKey("datasets.id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("version", Integer, nullable=False),
            Column("created_at", DateTime),
            UniqueConstraint("dataset_id", "version"),
        ]

    @staticmethod
    def storage_partial_columns() -> List["SchemaItem"]:
        return [
            Column("path_str", Text, primary_key=True, nullable=False),
            Column("timestamp", DateTime),
            Column("expires", DateTime),
        ]

    def get_storage_partial_table(self, name: str) -> Table:
        table = self.metadata.tables.get(name)
        if table is None:
            table = Table(
                name,
                self.metadata,
                *self.storage_partial_columns(),
            )
        return table

    @staticmethod
    def compile_glob(glob: str) -> str:
        """
        Returns compiled glob since some engines support special glob syntax
        """
        return glob

    @abstractmethod
    def clone(self, uri: Optional[str]) -> "AbstractDataStorage":
        """Clones DataStorage implementation for some Storage input"""

    @abstractmethod
    def init_db(self, prefix: str = "", is_new: bool = True):
        """Initializes database tables for data storage"""

    @abstractmethod
    def _rename_table(self, old_name: str, new_name: str):
        """Renames a table from old_name to new_name"""

    #
    # Query Tables
    #

    @property
    def nodes(self):
        assert (
            self.listing_table_name
        ), "Nodes can only be used if uri/listing_table_name is set"
        if self._nodes is None:
            self._nodes = self.schema.node_cls(self.listing_table_name, self.metadata)
        return self._nodes

    def dataset_rows(self, dataset_id: int, version: Optional[int] = None):
        name = self.dataset_table_name(dataset_id, version)
        return self.schema.dataset_row_cls(name, self.engine, self.metadata)

    @property
    def storages(self) -> Table:
        if self._storages is None:
            self._storages = Table(
                self.STORAGE_TABLE, self.metadata, *self.buckets_columns()
            )
        return self._storages

    @property
    def partials(self) -> Table:
        assert (
            self.listing_table_name
        ), "Partials can only be used if uri/listing_table_name is set"
        if self._partials is None:
            self._partials = self.get_storage_partial_table(
                f"{self.listing_table_name}_indexed"
            )
        return self._partials

    @property
    def datasets(self) -> Table:
        if self._datasets is None:
            self._datasets = Table(
                self.DATASET_TABLE, self.metadata, *self.datasets_columns()
            )
        return self._datasets

    @property
    def datasets_versions(self) -> Table:
        if self._datasets_versions is None:
            self._datasets_versions = Table(
                self.DATASET_VERSION_TABLE,
                self.metadata,
                *self.datasets_versions_columns(),
            )
        return self._datasets_versions

    #
    # Query Starters (These can be overridden by subclasses)
    #

    def storages_select(self, *columns):
        storages = self.storages
        if not columns:
            return storages.select()
        return select(*columns).select_from(storages)

    def storages_update(self):
        return self.storages.update()

    def storages_delete(self):
        return self.storages.delete()

    def partials_select(self, *columns):
        partials = self.partials
        if not columns:
            return partials.select()
        return select(*columns).select_from(partials)

    def partials_update(self):
        return self.partials.update()

    def partials_delete(self):
        return self.partials.delete()

    def datasets_select(self, *columns):
        datasets = self.datasets
        if not columns:
            return datasets.select()
        return select(*columns).select_from(datasets)

    def datasets_update(self):
        return self.datasets.update()

    def datasets_delete(self):
        return self.datasets.delete()

    def datasets_versions_select(self, *columns):
        datasets_versions = self.datasets_versions
        if not columns:
            return datasets_versions.select()
        return select(*columns).select_from(datasets_versions)

    def datasets_versions_update(self):
        return self.datasets_versions.update()

    def datasets_versions_delete(self):
        return self.datasets_versions.delete()

    #
    # Query Execution
    #

    @abstractmethod
    def execute(
        self, query, cursor: Optional[Any] = None, conn: Optional[Any] = None
    ) -> Iterator[Tuple[Any, ...]]:
        ...

    @abstractmethod
    def executemany(
        self, query, params, cursor: Optional[Any] = None
    ) -> Iterator[Tuple[Any, ...]]:
        ...

    #
    # Table Name Internal Functions
    #

    @classmethod
    def _table_name(cls, name, prefix) -> str:
        sha = hashlib.sha256(name.encode("utf-8")).hexdigest()
        return prefix + sha[: cls.TABLE_NAME_SHA_LIMIT]

    @classmethod
    def dataset_table_name(cls, dataset_id: int, version: Optional[int] = None) -> str:
        name = cls.DATASET_TABLE_PREFIX + str(dataset_id)
        if version is not None:
            name += f"_{version}"
        else:
            name += "_shadow"

        return name

    @property
    def listing_table_name(self) -> Optional[str]:
        if not self.uri:
            return None

        return self._table_name(self.uri, self.LISTING_TABLE_NAME_PREFIX)

    #
    # Storages
    #

    @abstractmethod
    def create_storage_if_not_registered(
        self, uri: str, symlinks: bool = False
    ) -> None:
        """
        Saves new storage if it doesn't exist in database
        """

    @abstractmethod
    def register_storage_for_indexing(
        self,
        uri: str,
        force_update: bool,
        prefix: str = "",
    ) -> Tuple[Storage, bool, bool, bool]:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        It returns:
            - storage, prepared for indexing
            - boolean saying if indexing is needed
            - boolean saying if indexing is currently pending (running)
            - boolean saying if this storage is newly created
        """

    @abstractmethod
    def find_stale_storages(self):
        """
        Finds all pending storages for which the last inserted node has happened
        before STALE_HOURS_LIMIT hours, and marks it as STALE
        """

    @abstractmethod
    def mark_storage_indexed(
        self,
        uri: str,
        status: int,
        ttl: int,
        end_time: Optional[datetime] = None,
        prefix: str = "",
    ) -> None:
        """
        Marks storage as indexed.
        This method should be called when index operation is finished
        """

    async def update_last_inserted_at(self, uri: Optional[str] = None) -> None:
        """Updates last inserted datetime in bucket with current time"""
        uri = uri or self.uri
        updates = {"last_inserted_at": datetime.now(timezone.utc)}
        s = self.storages
        self.execute(
            self.storages_update()
            .where(s.c.uri == uri)
            .values(**updates)  # type: ignore [attr-defined]
        )

    def get_all_storage_uris(self) -> Iterator[str]:
        s = self.storages
        yield from (r[0] for r in self.execute(self.storages_select(s.c.uri)))

    def get_storage(self, uri: str) -> Storage:
        """
        Gets storage representation from database.
        E.g if s3 is used as storage this would be s3 bucket data
        """
        s = self.storages
        result = next(self.execute(self.storages_select().where(s.c.uri == uri)), None)
        if not result:
            raise StorageNotFoundError(f"Storage {uri} not found.")

        return self.storage_class._make(result)

    def mark_storage_pending(self, storage: Storage) -> Storage:
        # Update status to pending and dates
        updates = {
            "status": StorageStatus.PENDING,
            "timestamp": None,
            "expires": None,
            "last_inserted_at": None,
            "started_inserting_at": datetime.now(timezone.utc),
        }
        storage = storage._replace(**updates)  # type: ignore [arg-type]
        s = self.storages
        self.execute(
            self.storages_update()
            .where(s.c.uri == storage.uri)
            .values(**updates)  # type: ignore [attr-defined]
        )
        return storage

    def _mark_storage_stale(self, storage_id: int) -> None:
        # Update status to pending and dates
        updates = {"status": StorageStatus.STALE, "timestamp": None, "expires": None}
        s = self.storages
        self.execute(
            self.storages.update()
            .where(s.c.id == storage_id)
            .values(**updates)  # type: ignore [attr-defined]
        )

    #
    # Partial Indexes
    #

    def _delete_partial_index(self, prefix: str):
        """
        Deletes the provided and any subdir indexed prefixes and nodes
        """
        bare_prefix = prefix.rstrip("/")
        dir_prefix = posixpath.join(prefix, "")
        p = self.partials
        self.execute(
            self.partials_delete().where(
                p.c.path_str.startswith(dir_prefix, autoescape=True)
            )
        )
        n = self.nodes
        self.execute(
            self.nodes.delete().where(
                n.c.path_str.startswith(dir_prefix, autoescape=True)
                | (n.c.path_str == bare_prefix)
            )
        )

    def _check_partial_index_valid(self, prefix: str):
        # This SQL statement finds all matching path_str entries that are
        # prefixes of the provided prefix, matching this or parent directories
        # that are indexed.
        dir_prefix = posixpath.join(prefix, "")
        p = self.partials
        expire_values = self.execute(
            self.partials_select(p.c.expires).where(
                p.c.path_str == func.substr(dir_prefix, 1, func.length(p.c.path_str))
            )
        )
        return not all(is_expired(expires[0]) for expires in expire_values)

    #
    # Datasets
    #

    @abstractmethod
    def create_dataset_rows_table(
        self,
        name: str,
        custom_columns: Sequence["sa.Column"] = (),
        if_not_exists: bool = True,
    ) -> None:
        """Creates a dataset rows table for the given dataset name and columns"""

    @abstractmethod
    def create_shadow_dataset(
        self, name: str, create_rows: Optional[bool] = True
    ) -> "DatasetRecord":
        """
        Creates shadow database record if doesn't exist.
        If create_rows is False, dataset rows table will not be created
        """

    @abstractmethod
    def insert_into_shadow_dataset(
        self, name: str, uri: str, path: str, recursive: bool = False
    ) -> None:
        """Inserts data to shadow dataset based on bucket uri and glob path"""

    @abstractmethod
    def create_dataset_version(
        self, name: str, version: int, create_rows_table=True
    ) -> "DatasetRecord":
        """Creates new dataset version, optionally creating new rows table"""

    @abstractmethod
    def merge_dataset_rows(
        self,
        src: "DatasetRecord",
        dst: "DatasetRecord",
        src_version: Optional[int] = None,
        dst_version: Optional[int] = None,
    ) -> None:
        """
        Merges source dataset rows and current latest destination dataset rows
        into a new rows table created for new destination dataset version.
        Note that table for new destination version must be created upfront.
        Merge results should not contain duplicates.
        """

    @abstractmethod
    def remove_shadow_dataset(self, dataset: "DatasetRecord", drop_rows=True) -> None:
        """
        Removes shadow dataset and it's corresponding rows if needed
        """

    @abstractmethod
    def _get_dataset_row_values(
        self,
        name: str,
        columns: Optional[Sequence[str]] = None,
        limit: Optional[int] = 20,
        version=None,
    ) -> Iterator[Mapping[str, Any]]:
        """Gets dataset row values for the provided columns"""

    def get_dataset_rows(
        self, name: str, limit: Optional[int] = 20, version=None
    ) -> Iterator[DatasetRow]:
        """Gets dataset rows"""
        for row in self._get_dataset_row_values(
            name, columns=DATASET_CORE_COLUMN_NAMES, limit=limit, version=version
        ):
            yield DatasetRow(**row)

    def get_dataset_row(
        self,
        name: str,
        row_id: int,
        dataset_version: Optional[int] = None,
    ) -> Optional[DatasetRow]:
        """Returns one row by id from a defined dataset"""
        dataset = self.get_dataset(name)

        dr = self.dataset_rows(dataset.id, dataset_version)
        row = next(
            self.execute(dr.select().where(dr.c.id == row_id)),
            None,
        )
        if row:
            return DatasetRow(*row)

        return None

    def nodes_dataset_query(
        self,
        columns: Optional[Iterable[str]] = None,
        path: Optional[str] = None,
        recursive: Optional[bool] = False,
        uri: Optional[str] = None,
    ) -> "sa.Select":
        """
        Provides a query object representing the given `uri` as a dataset.

        If `uri` is not given then `self.uri` is used. The given `columns`
        will be selected in the order they're given. `path` is a glob which
        will select files in matching directories, or if `recursive=True` is
        set then the entire tree under matching directories will be selected.
        """
        if uri is not None:
            # TODO refactor to avoid setting self.uri here
            self.uri = uri.rstrip("/")  # Needed for parent node and .nodes
        if columns is None:
            columns = DATASET_CORE_COLUMN_NAMES
        n = self.nodes
        column_objects = [
            sa.literal(self.uri).label("source") if c == "source" else n.c[c]
            for c in columns
        ]
        select_query = self.nodes.select(*column_objects)
        if path is None:
            return self.add_node_type_where(select_query, "file")
        if recursive:
            if not path.endswith("*"):
                path = path.rstrip("/")
                if path:
                    # setting sufix for globs only if path is defined
                    path = path + "/*"  # glob filter must end with /*

            if path:
                select_query = select_query.where(
                    (n.c.path_str.op(self.glob_op)(self.compile_glob(path)))
                    & (n.c.valid == true())
                    & (n.c.is_latest == true())
                )
            else:
                # we are getting the whole storage, no need to query by path
                select_query = select_query.where(
                    (n.c.valid == true()) & (n.c.is_latest == true())
                )
        else:
            parent = self.get_node_by_path(path.lstrip("/").rstrip("/*"))
            select_query = select_query.where(
                (n.c.parent_id == parent.id)
                & (n.c.valid == true())
                & (n.c.is_latest == true())
            )
        return self.add_node_type_where(select_query, "file")

    def rename_dataset_table(
        self,
        old_name: str,
        new_name: str,
        old_version: Optional[int] = None,
        new_version: Optional[int] = None,
    ) -> None:
        """
        When registering dataset, we need to rename rows table from
        ds_<id>_shadow to ds_<id>_<version>.
        Example: from ds_24_shadow to ds_24_1
        """
        old_dataset = self.get_dataset(old_name)
        new_dataset = self.get_dataset(new_name)

        old_name = self.dataset_table_name(old_dataset.id, old_version)
        new_name = self.dataset_table_name(new_dataset.id, new_version)

        self._rename_table(old_name, new_name)

    def update_dataset(self, dataset_name: str, conn=None, **kwargs) -> None:
        """Updates dataset fields"""
        values = {}
        for field, value in kwargs.items():
            if field in self.dataset_fields[1:]:
                if field == "labels":
                    values[field] = json.dumps(value) if value else None
                else:
                    values[field] = value

        if not values:
            # Nothing to update
            return

        d = self.datasets
        self.execute(
            self.datasets_update().where(d.c.name == dataset_name).values(values),
            conn=conn,
        )  # type: ignore [attr-defined] # noqa: E501

    def _parse_dataset(self, rows) -> Optional[DatasetRecord]:
        versions = []
        for r in rows:
            versions.append(self.dataset_class.parse(*r))
        if not versions:
            return None
        return reduce(lambda ds, version: ds.merge_versions(version), versions)

    def remove_dataset_version(self, dataset: DatasetRecord, version: int) -> None:
        """
        Deletes one single dataset version. If it was last version,
        it removes dataset completely
        """
        if not dataset.has_version(version):
            return

        d = self.datasets
        dv = self.datasets_versions
        self.execute(
            self.datasets_versions_delete().where(
                (dv.c.dataset_id == dataset.id) & (dv.c.version == version)
            )
        )

        if dataset.versions and len(dataset.versions) == 1:
            # had only one version, fully deleting dataset
            self.execute(self.datasets_delete().where(d.c.id == dataset.id))

        dataset.remove_version(version)

        table_name = self.dataset_table_name(dataset.id, version)
        table = Table(table_name, MetaData())
        table.drop(self.engine)

    def list_datasets(
        self, shadow_only: Optional[bool] = None
    ) -> Iterator["DatasetRecord"]:
        """Lists all datasets (or shadow datasets only)"""
        d = self.datasets
        dv = self.datasets_versions
        query = self.datasets_select(
            *(getattr(d.c, f) for f in self.dataset_fields), dv.c.version
        ).join(dv, d.c.id == dv.c.dataset_id, isouter=True)

        if shadow_only is not None:
            query = query.where(  # type: ignore [attr-defined]
                d.c.shadow == bool(shadow_only)
            )

        for _, g in groupby(self.execute(query), operator.itemgetter(0)):
            dataset = self._parse_dataset(list(g))
            if dataset:
                yield dataset

    def get_dataset(self, name: str) -> DatasetRecord:
        """Gets a single dataset by name"""
        d = self.datasets
        dv = self.datasets_versions
        query = (
            self.datasets_select(
                *(getattr(d.c, f) for f in self.dataset_fields), dv.c.version
            )
            .join(dv, d.c.id == dv.c.dataset_id, isouter=True)
            .where(d.c.name == name)  # type: ignore [attr-defined]
        )
        ds = self._parse_dataset(self.execute(query))
        if not ds:
            raise DatasetNotFoundError(f"Dataset {name} not found.")
        return ds

    def update_dataset_status(
        self, dataset: DatasetRecord, status: int, conn=None
    ) -> DatasetRecord:
        """
        Updates dataset status and appropriate fields related to status
        """
        update_data: Dict[str, Any] = {"status": status}
        if status in [DatasetStatus.COMPLETE, DatasetStatus.FAILED]:
            # if in final state, updating finished_at datetime
            update_data["finished_at"] = datetime.now(timezone.utc)

        self.update_dataset(dataset.name, conn=conn, **update_data)
        dataset.update(**update_data)
        return dataset

    #
    # Nodes
    #

    @abstractmethod
    def validate_paths(self) -> int:
        """Find and mark any invalid paths."""

    @abstractmethod
    async def insert_entry(self, entry: Dict[str, Any]) -> int:
        """
        Inserts file or directory node into the database
        and returns the id of the newly added node
        """

    @abstractmethod
    async def insert_entries(self, entries: Iterable[Dict[str, Any]]) -> None:
        """Inserts file or directory nodes into the database"""

    async def insert_root(self) -> int:
        """
        Inserts root directory and returns the id of the newly added root
        """
        return await self.insert_entry({"dir_type": DirType.ROOT})

    def _prepare_node(self, d: Dict[str, Any]) -> Dict[str, Any]:
        if d.get("dir_type") is None:
            if d.get("is_root"):
                dir_type = DirType.ROOT
            elif d.get("is_dir"):
                dir_type = DirType.DIR
            else:
                dir_type = DirType.FILE
            d["dir_type"] = dir_type

        if not d.get("path_str"):
            if d.get("path"):
                path = d["path"]
                if isinstance(path, list):
                    d["path_str"] = "/".join(path)
                else:
                    d["path_str"] = path
            elif d.get("dir_type") == DirType.ROOT:
                d["path_str"] = ""
            else:
                raise RuntimeError(f"No Path for node data: {d}")

        d = {
            "name": "",
            "is_latest": True,
            "size": 0,
            "valid": True,
            "random": getrandbits(RANDOM_BITS),
            **d,
        }
        return {f: d.get(f) for f in self.node_fields[1:]}

    def add_node_type_where(self, query, type):  # pylint: disable=redefined-builtin
        if type in {"f", "file", "files"}:
            return query.where(self.nodes.c.dir_type == DirType.FILE)
        elif type in {"d", "dir", "directory", "directories"}:
            return query.where(self.nodes.c.dir_type != DirType.FILE)
        return query

    def get_nodes(self, query) -> Iterator[Node]:
        """
        This gets nodes based on the provided query, and should be used sparingly,
        as it will be slow on any OLAP database systems.
        """
        return map(Node._make, self.execute(query))

    def get_nodes_by_parent_id(
        self,
        parent_id: int,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterator[Node]:
        """Gets nodes from database by parent_id, with optional filtering"""
        n = self.nodes
        query = self.nodes.select().where(
            (n.c.valid == true())
            & (n.c.is_latest == true())
            & (n.c.parent_id == parent_id)
        )
        query = self.add_node_type_where(query, type)
        return self.get_nodes(query)

    def _get_nodes_by_glob_path_pattern(
        self, path_list: List[str], glob_name: str
    ) -> Iterator[NodeWithPath]:
        """Finds all Nodes that correspond to GLOB like path pattern."""
        node = self._get_node_by_path_list(path_list)
        if not node.is_dir:
            raise RuntimeError(f"Can't resolve name {'/'.join(path_list)}")

        def _with_path(row):
            return NodeWithPath(*row, path_list)  # type: ignore [call-arg]

        n = self.nodes
        return map(
            _with_path,
            self.get_nodes(
                self.nodes.select().where(
                    (n.c.parent_id == node.id)
                    & (n.c.name.op(self.glob_op)(self.compile_glob(glob_name)))
                    & (n.c.valid == true())
                    & (n.c.is_latest == true())
                )
            ),
        )

    def _get_node_by_path_list(self, path_list: List[str]) -> NodeWithPath:
        """
        Gets node that correspond some path list, e.g ["data-lakes", "dogs-and-cats"]
        """
        path_str = "/".join(path_list)
        n = self.nodes
        row = next(
            self.execute(
                self.nodes.select()
                .where(
                    (n.c.path_str == path_str)
                    & (n.c.valid == true())
                    & (n.c.is_latest == true())
                )
                .order_by("dir_type")  # type: ignore [attr-defined]
            ),
            None,
        )
        if not row:
            raise FileNotFoundError(f"Unable to resolve path {path_str}")
        return NodeWithPath(*row, row[self.path_str_index].split("/"))  # type: ignore [call-arg] # noqa: E501

    def _populate_nodes_by_path(
        self, path_list: List[str], num: int, res: List[NodeWithPath]
    ) -> None:
        """
        Puts all nodes found by path_list into the res input variable.
        Note that path can have GLOB like pattern matching which means that
        res can have multiple nodes as result.
        If there is no GLOB pattern, res should have one node as result that
        match exact path by path_list
        """
        if num >= len(path_list):
            res.append(self._get_node_by_path_list(path_list))
            return

        curr_name = path_list[num]
        if set(curr_name).intersection(GLOB_CHARS):
            nodes = self._get_nodes_by_glob_path_pattern(path_list[:num], curr_name)
            for node in nodes:
                if not node.is_dir:
                    res.append(node)
                else:
                    path = (
                        path_list[:num]
                        + [node.name or ""]
                        + path_list[num + 1 :]  # type: ignore [attr-defined]
                    )
                    self._populate_nodes_by_path(path, num + 1, res)
        else:
            self._populate_nodes_by_path(path_list, num + 1, res)
            return
        return

    def get_node_by_path(self, path: str) -> NodeWithPath:
        """Gets node that corresponds to some path"""
        n = self.nodes
        query = self.nodes.select().where(
            (n.c.path_str == path.strip("/"))
            & (n.c.valid == true())
            & (n.c.is_latest == true())
        )
        if path.endswith("/"):
            query = self.add_node_type_where(query, "dir")
        row = next(self.execute(query), None)
        if not row:
            raise FileNotFoundError(f"Unable to resolve path {path}")
        return NodeWithPath(*row, row[self.path_str_index].split("/"))  # type: ignore [call-arg] # noqa: E501

    def expand_path(self, path: str) -> List[NodeWithPath]:
        """Simulates Unix-like shell expansion"""
        clean_path = path.strip("/")
        path_list = clean_path.split("/") if clean_path != "" else []

        res: List[NodeWithPath] = []
        self._populate_nodes_by_path(path_list, 0, res)
        return res

    def select_nodes_fields_by_parent(
        self, parent_node: Node, fields: Iterable[str]
    ) -> Iterator[Tuple[Any, ...]]:
        """
        Gets latest-version file nodes from the provided parent node
        """
        if not parent_node.is_dir:
            return iter([tuple(getattr(parent_node, f) for f in fields)])

        n = self.nodes
        return self.execute(
            self.nodes.select(*(getattr(n.c, f) for f in fields)).where(
                (n.c.parent_id == parent_node.id)
                & (n.c.valid == true())
                & (n.c.is_latest == true())
            )
        )

    def size(
        self, node: Union[AnyNode, Dict[str, Any]], count_files: bool = False
    ) -> Tuple[int, int]:
        """
        Calculates size of some node (and subtree below node).
        Returns size in bytes as int and total files as int
        """
        if isinstance(node, dict):
            is_dir = node.get("is_dir", node["dir_type"] != DirType.FILE)
            node_size = node["size"]
            path_str = node["path_str"]
        else:
            is_dir = node.is_dir
            node_size = node.size
            path_str = node.path_str
        if not is_dir:
            # Return node size if this is not a directory
            return node_size, 1

        sub_glob = posixpath.join(path_str, "*")
        n = self.nodes
        selections = [
            func.sum(n.c.size),  # pylint: disable=not-callable
        ]
        if count_files:
            selections.append(
                func.sum(n.c.dir_type == 0),  # pylint: disable=not-callable
            )
        results = next(
            self.execute(
                self.nodes.select(*selections).where(
                    (n.c.path_str.op(self.glob_op)(self.compile_glob(sub_glob)))
                    & (n.c.valid == true())
                    & (n.c.is_latest == true())
                )
            ),
            (0, 0),
        )
        if count_files:
            return results[0] or 0, results[1] or 0
        else:
            return results[0] or 0, 0

    def _find_query(
        self,
        node: AnyNode,
        query,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        conds=None,
    ):
        if not conds:
            conds = []

        n = self.nodes

        if node.path_str:
            sub_glob = posixpath.join(node.path_str, "*")
            conds.append(n.c.path_str.op("GLOB")(sub_glob))

        query = query.where(
            and_(
                *conds,
                n.c.dir_type != DirType.ROOT,
                n.c.valid == true(),
                n.c.is_latest == true(),
            )
        )
        if type is not None:
            query = self.add_node_type_where(query, type)

        return query

    def walk_subtree(
        self,
        node: AnyNode,
        sort: Union[List[str], str, None] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterator[NodeWithPath]:
        """
        Returns all directory and file nodes that are "below" some node.
        Nodes can be sorted or filtered as well.
        """
        query = self._find_query(node, self.nodes.select(), type)

        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
            query = query.order_by(*(sa.text(s) for s in sort))  # type: ignore [attr-defined] # noqa: E501

        prefix_len = len(node.path_str)

        def make_node_with_path(row):
            return NodeWithPath(
                *row, row[self.path_str_index][prefix_len:].lstrip("/").split("/")
            )

        return map(make_node_with_path, self.execute(query))  # type: ignore [call-arg]

    def find(
        self,
        node: AnyNode,
        fields: Iterable[str],
        jmespath: str = "",
        type=None,  # pylint: disable=redefined-builtin
        conds=None,
    ) -> Iterator[Tuple[Any, ...]]:
        """
        Finds nodes that match certain criteria like name or jmespath,
        and only looks for latest nodes under the passed node.
        """
        if jmespath:
            raise NotImplementedError("jmespath queries not supported!")

        n = self.nodes
        query = self._find_query(
            node, self.nodes.select(*(getattr(n.c, f) for f in fields)), type, conds
        )
        return self.execute(query)

    def update_checksum(self, node: AnyNode, checksum: str) -> None:
        """Updates checksum of specific node in database"""
        n = self.nodes
        self.execute(
            self.nodes.update()
            .where(n.c.id == node.id)
            .values(checksum=checksum)  # type: ignore [attr-defined]
        )
