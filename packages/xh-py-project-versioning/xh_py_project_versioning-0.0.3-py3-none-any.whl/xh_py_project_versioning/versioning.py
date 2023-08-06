import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class SemVer:
    major: int
    minor: int
    patch: int
    pre_release: Optional[str]
    build: Optional[int]

    def increase_major(self):
        self.major = self.major+1

    def increase_minor(self):
        self.minor = self.minor+1

    def increase_patch(self):
        self.patch = self.patch+1

    def set_pre_release(self, pre_release: str):
        self.pre_release = pre_release

    def unset_pre_release(self):
        self.set_pre_release(None)

    def increase_build(self):
        self.build = 1 if self.build is None else self.build+1

    def set_build(self, build: Optional[int]):
        self.build = build

    def unset_build(self):
        self.build = None

    def is_pre_release_not_set(self):
        return not self.is_pre_release_set()

    def is_pre_release_set(self):
        if self.pre_release is None:
            return False
        else:
            return True

    def __str__(self):
        pre_release_str = f"-{self.pre_release}" if self.pre_release is not None else ""
        build_str = f"+{self.build:03d}" if self.build is not None else ""
        return f"{self.major}.{self.minor}.{self.patch}{pre_release_str}{build_str}"

    def __repr__(self):
        self.__str__()

    @staticmethod
    def from_str(sem_ver_string: str) -> 'SemVer':
        pattern = re.compile("^(\\d+)\\.(\\d+)\\.(\\d+)(-dev)?(\\+[^ ]+)?$")
        matcher = pattern.match(sem_ver_string)
        if matcher:
            major = int(matcher.group(1))
            minor = int(matcher.group(2))
            patch = int(matcher.group(3))
            pre_release = matcher.group(4)[1:] if matcher.group(4) else None
            build = int(matcher.group(5)[1:]) if matcher.group(5) else None
            return SemVer(major, minor, patch, pre_release, build)
        else:
            raise Exception("not match version")


