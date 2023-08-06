import os
import posixpath
from datetime import datetime
from typing import List, NamedTuple, Optional, Union

from dql.utils import time_to_str


class DirType:
    FILE = 0
    DIR = 1
    ROOT = 2
    TAR = 3  # TAR archive member


class NodeRecord(NamedTuple):
    id: int = 0
    dir_type: Optional[int] = None
    parent_id: Optional[int] = None
    name: Optional[str] = None
    checksum: str = ""
    etag: str = ""
    version: Optional[str] = None
    is_latest: bool = True
    last_modified: Optional[datetime] = None
    size: int = 0
    owner_name: str = ""
    owner_id: str = ""
    path_str: str = ""
    anno: Optional[str] = None
    valid: bool = True
    random: int = -1
    sub_meta: Optional[str] = None


_fields = list(NodeRecord.__annotations__.items())  # pylint:disable=no-member
NodeRecordWithPath = NamedTuple(  # type: ignore
    "NodeRecordWithPath",
    _fields + [("path", List[str])],
)


class AbstractNode:
    # pylint: disable=no-member
    TIME_FMT = "%Y-%m-%d %H:%M"

    @property
    def id(self) -> int:
        return self.id

    @property
    def is_dir(self) -> bool:
        return bool(self.dir_type)

    @property
    def dir_type(self) -> Optional[int]:
        return self.dir_type

    @property
    def path_str(self) -> str:
        return self.path_str

    @property
    def dirname(self) -> str:
        return self.path_str if self.is_dir else posixpath.dirname(self.path_str)

    @property
    def name(self) -> Optional[str]:
        return self.name

    @property
    def owner_name(self) -> Optional[str]:
        return self.owner_name

    @property
    def name_no_ext(self) -> str:
        if not self.name:
            return ""
        name, _ = os.path.splitext(self.name)
        return name

    @property
    def is_downloadable(self) -> bool:
        return bool(not self.is_dir and self.name)

    @property
    def size(self) -> int:
        return self.size or 0

    def get_metafile_data(self):
        data = {
            "name": "/".join(self.path),
            "etag": self.etag,
        }
        checksum = self.checksum
        if checksum:
            data["checksum"] = checksum
        version = self.version
        if version:
            data["version"] = version
        data["last_modified"] = time_to_str(self.last_modified)
        data["size"] = self.size
        return data

    def append_to_file(self, fd):
        fd.write(f"- name: {'/'.join(self.path)}\n")
        fd.write(f"  etag: {self.etag}\n")
        checksum = self.checksum
        if checksum:
            fd.write(f"  checksum: {self.checksum}\n")
        version = self.version
        if version:
            fd.write(f"  version: {self.version}\n")
        fd.write(f"  last_modified: '{time_to_str(self.last_modified)}'\n")
        size = self.size
        fd.write(f"  size: {self.size}\n")
        return size

    def sql_schema(self):
        return ",".join(["?"] * len(self))


class Node(NodeRecord, AbstractNode):
    @property
    def full_path(self):
        if self.is_dir and self.path_str:
            return self.path_str + "/"
        return self.path_str


class NodeWithPath(  # pylint:disable=inherit-non-class
    NodeRecordWithPath,
    AbstractNode,
):
    @property
    def full_path(self):
        path = posixpath.join(*self.path) if self.path else ""
        if self.is_dir and path:
            path += "/"
        return path


AnyNode = Union[Node, NodeWithPath]


def long_line_str(name: str, timestamp: Optional[datetime], owner: str) -> str:
    if timestamp is None:
        time = "-"
    else:
        time = timestamp.strftime(AbstractNode.TIME_FMT)
    return f"{owner: <19} {time: <19} {name}"
