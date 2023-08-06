import json
import tarfile
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Iterator, Tuple

from dql.node import DirType

if TYPE_CHECKING:
    from .catalog import DataSource


class IndexingFormat(ABC):
    """
    Indexing formats allow additional transformations on indexed
    objects, such as listing contents of archives.
    """

    @abstractmethod
    def filter(self, source: "DataSource") -> Iterator[Tuple[Any, ...]]:
        """Determine whether an entry needs processing."""

    @abstractmethod
    def process(self, source, entry):
        """Process an entry and return additional entries to store."""


class Webdataset(IndexingFormat):
    """
    Webdataset indexes buckets containing uncompressed tar archives. The contents of
    the archives is indexed as well.
    """

    def filter(self, source: "DataSource") -> Iterator[Tuple[Any, ...]]:
        return source.listing.find(
            source.node,
            ["path_str", "id", "is_latest"],
            names=["*.tar"],
        )

    def process(self, source, entry):
        pth, parent_id, is_latest = entry
        with source.listing.client.open(pth) as f:
            with tarfile.open(fileobj=f, mode="r") as tar:
                for info in tar:
                    if info.isdir():
                        continue
                    yield self.tarmember_from_info(info, parent_id, pth, is_latest)

    def tarmember_from_info(self, info, parent_id, path_str, is_latest):
        sub_meta = json.dumps({"offset": info.offset_data})
        return {
            "dir_type": DirType.TAR,
            "parent_id": parent_id,
            "path_str": f"{path_str}/{info.name}",
            "name": info.name,
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": is_latest,
            "last_modified": datetime.fromtimestamp(info.mtime, timezone.utc),
            "size": info.size,
            "owner_name": info.uname,
            "owner_id": info.uid,
            "sub_meta": sub_meta,
        }


indexer_formats: Dict[str, IndexingFormat] = {
    "webdataset": Webdataset(),
}
