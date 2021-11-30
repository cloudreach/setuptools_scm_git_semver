import re
from typing import NamedTuple, Optional, Sequence, Tuple

import setuptools_scm.version

RC_RE = re.compile(r"rc.(?P<number>\d+)")


class VersionCore(NamedTuple):
    major: int
    minor: int
    patch: int

    def set(
        self, major: int = None, minor: int = None, patch: int = None
    ) -> "VersionCore":
        return VersionCore(
            self.major if major is None else major,
            self.minor if minor is None else minor,
            self.patch if patch is None else patch,
        )

    @classmethod
    def from_str(cls, version) -> "VersionCore":
        return cls(*(int(x) for x in version.split(".")))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


class _Semver(NamedTuple):
    version_core: VersionCore
    pre_release: Sequence[str]
    build: str

    def set(
        self,
        version_core: VersionCore = None,
        pre_release: Sequence[str] = None,
        build: str = None,
    ) -> "_Semver":
        return _Semver(
            self.version_core if version_core is None else version_core,
            self.pre_release if pre_release is None else pre_release,
            self.build if build is None else build,
        )

    def get_rc(self) -> Tuple["_Semver", Optional[int]]:
        for index, pr in enumerate(self.pre_release):
            match = RC_RE.match(pr)
            if match:
                rc = int(match.group("number"))
                head, (_, *tail) = self.pre_release[:index], self.pre_release[index:]
                return (
                    _Semver(
                        self.version_core,
                        (*head, *tail),
                        self.build,
                    ),
                    rc,
                )
        return self, None

    @classmethod
    def from_tag(cls, tag: str) -> "_Semver":
        public, _, build = tag.partition("+")
        core, _, pre = public.partition("-")
        return cls(VersionCore.from_str(core), pre.split("-") if pre else (), build)

    def __str__(self) -> str:
        parts = [str(self.version_core)]
        if self.pre_release:
            parts += f"-{'-'.join(self.pre_release)}"
        if self.build:
            parts += f"+{self.build}"
        return "".join(parts)


def guess_next_rc(version: setuptools_scm.version.ScmVersion) -> str:
    """Next RC unless we are on an exact version."""
    if version.exact and not version.dirty:
        return str(version.format_with("{tag}"))
    semver, rc = _Semver.from_tag(str(version.tag)).get_rc()
    if rc is None:
        return str(
            semver.set(
                version_core=semver.version_core.set(
                    patch=semver.version_core.patch + 1
                ),
                pre_release=(*semver.pre_release, "rc.0"),
            )
        )
    return str(semver.set(pre_release=(*semver.pre_release, f"rc.{rc + 1}")))


def local_time_dot_node(version: setuptools_scm.version.ScmVersion) -> str:
    """The datetime if dirty; the datetime.node if not on a tag."""
    # the t and z are lowercase on purpose: Setuptools warns if they are not
    time_format = "%Y%m%dt%H%M%Sz"
    if version.exact or version.node is None:
        return str(
            version.format_choice("", "+d{time:{time_format}}", time_format=time_format)
        )
    return str(
        version.format_with("+{time:{time_format}}.{node}", time_format=time_format)
    )
