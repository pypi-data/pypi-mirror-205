import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Type, TypeVar

import attrs
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    Table,
    Text,
)

T = TypeVar("T", bound="DatasetRecord")


class Status:
    CREATED = 1
    PENDING = 2
    FAILED = 3
    COMPLETE = 4
    STALE = 6


@dataclass
class DatasetRecord:
    id: int
    name: str
    description: Optional[str]
    labels: Sequence[str]
    shadow: bool
    versions: Optional[List[int]]
    status: int = Status.CREATED
    created_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    @classmethod
    def parse(
        cls: Type[T],
        id: int,  # pylint: disable=redefined-builtin
        name: str,
        description: Optional[str],
        labels: str,
        shadow: int,
        status: int,
        created_at: datetime,
        finished_at: Optional[datetime],
        version: Optional[int],
    ) -> "DatasetRecord":
        labels_lst: List[str] = json.loads(labels) if labels else []
        versions = None
        if version:
            versions = [version]

        return cls(
            id,
            name,
            description,
            labels_lst,
            bool(shadow),
            versions,
            status,
            created_at,
            finished_at,
        )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def merge_versions(self, other: "DatasetRecord") -> "DatasetRecord":
        """Merge versions from another dataset"""
        if other.id != self.id:
            raise RuntimeError("Cannot merge versions of datasets with different ids")
        if not other.versions:
            # nothing to merge
            return self
        if not self.versions:
            self.versions = []

        self.versions = list(set(self.versions + other.versions))
        return self

    def has_version(self, version: int) -> bool:
        if not self.versions:
            return False
        return version in self.versions

    def is_valid_next_version(self, version: int) -> bool:
        """
        Checks if a number can be a valid next latest version for dataset.
        The only rule is that it cannot be lower than current latest version
        """
        if self.latest_version and self.latest_version >= version:
            return False
        return True

    def remove_version(self, version: int) -> None:
        if not self.versions or not self.has_version(version):
            return

        self.versions.remove(version)

    @property
    def registered(self) -> bool:
        return not self.shadow

    @property
    def next_version(self) -> int:
        """Returns what should be next autoincrement version of dataset"""
        if self.shadow or not self.versions:
            return 1
        return max(self.versions) + 1

    @property
    def latest_version(self) -> Optional[int]:
        """Returns latest version of a dataset"""
        if self.shadow or not self.versions:
            return None
        return max(self.versions)

    @property
    def prev_version(self) -> Optional[int]:
        """Returns previous version of a dataset"""
        if self.shadow or not self.versions or len(self.versions) == 1:
            return None

        return sorted(self.versions)[-2]


@attrs.define
class DatasetRow:
    id: int
    dir_type: int
    parent_id: Optional[int]
    name: str
    checksum: str
    etag: str
    version: str
    is_latest: bool
    last_modified: Optional[datetime]
    size: int
    owner_name: str
    owner_id: str
    path_str: str
    anno: Optional[str]
    source: str
    random: int
    sub_meta: Optional[str] = None
    custom: Optional[Dict] = {}

    @classmethod
    def from_cursor(cls, cursor, values):
        cols = [c[0] for c in cursor.description]
        row = dict(zip(cols, values))
        core_fields = {key: value for (key, value) in row.items() if hasattr(cls, key)}
        custom_fields = {
            key: value for (key, value) in row.items() if key not in core_fields
        }
        return cls(**core_fields, custom=custom_fields)

    def __getitem__(self, col):
        if hasattr(self, col):
            return getattr(self, col)
        elif self.custom and col in self.custom:
            return self.custom[col]
        raise KeyError


def dataset_table(name: str, custom_columns: Sequence["Column"] = ()):
    return Table(
        name,
        MetaData(),
        *core_dataset_columns(),
        *custom_columns,
    )


def core_dataset_columns() -> List["Column"]:
    return [
        Column("id", Integer, primary_key=True),
        Column("dir_type", Integer),
        Column("parent_id", Integer),
        Column("name", Text, nullable=False),
        Column("checksum", Text),
        Column("etag", Text),
        Column("version", Text),
        Column("is_latest", Boolean),
        Column("last_modified", DateTime),
        Column("size", BigInteger, nullable=False),
        Column("owner_name", Text),
        Column("owner_id", Text),
        Column("path_str", Text),
        Column("anno", JSON),
        Column("source", Text, nullable=False),
        Column("random", BigInteger, nullable=False),
        Column("sub_meta", JSON),
    ]


DATASET_CORE_COLUMN_NAMES = [col.name for col in core_dataset_columns()]
