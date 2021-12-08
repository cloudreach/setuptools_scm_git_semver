# `setuptools_scm_git_semver`

[SemVer]-compatible hooks for [`setuptools_scm`].

This package was created because `setuptools_scm` produces [PEP 440] compliant version numbers,
which are not always compatible with SemVer.

## Usage

Usage is no different from normal setuptools_scm -- this package just adds 1
version scheme and local scheme each:

- `guess-next-rc`: Returns the next version as RC when not on a clean tag

- `time-dot-node`: Returns a local version of +<time>.<node>

In addition, if a version tag from SCM is not available, the content of
VERSION.txt is used.

Example configurations to get version numbers that are both valid python
package versions and SemVer versions, and fall back on what's in VERSION.txt if
not in SCM:

Using pyproject.toml:

```toml
[build-system]
requires = [
    "setuptools",
    "setuptools_scm",
    "setuptools_scm_git_semver",
]
build-backend = 'setuptools.build_meta'

[tool.setuptools_scm]
version_scheme = "guess-next-rc"
local_scheme = "time-dot-node"
normalize = false
write_to = "VERSION.txt"
```

## Releases

The package should be released to PyPI. The first release will be performed manually, and CI will be
written later.


[SemVer]: https://semver.org
[`setuptools_scm`]: https://github.com/pypa/setuptools_scm
[PEP 440]: https://www.python.org/dev/peps/pep-0440/#version-scheme
