# `setuptools_scm_git_semver`

[SemVer]-compatible hooks for [`setuptools_scm`].

This package was created because `setuptools_scm` produces [PEP 440] compliant version numbers,
which are not compatible with SemVer.

## Installation

Install using [pip], e.g.

```sh
pip install setuptools_scm_git_semver
```

## Usage

To configure `setuptools` to generate SemVer compatible numbers through `setuptools_scm` you could
use:

```py
# setup.py
from setuptools import setup
from setuptools_scm_git_semver import parse

setup(
    ...
    use_scm_version={
        'parse': parse,
        'version_scheme': 'semver',
        'local_scheme': 'semver'
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_semver'],
    ...
)

# $ python setup.py --version
# 1.2.4-rc.0.20190927T181700Z+ddb8be7
```

To retrieve the same version programmatically you could instead use:

```py
from setuptools_scm_git_semver import get_version

get_version()
# 1.2.4-rc.0.20190927T181700Z+ddb8be7
```

## Developing

There are no tests for this, so be careful. I'm not proud – I just want SemVer versions!

## Releases

The package should be released to PyPI. The first release will be performed manually, and CI will be
written later.

## API

This package defines a [`parse`] function, as well as [`version_scheme`] and [`local_scheme`]
implementations that together can create valid SemVer version numbers from git. See the
[configuration documentation] for how to configure `setuptools_scm` to use these.

Additionally, there is a [`get_version`] convenience function that obtains a version number using
the configuration in this package.

### Entrypoints

#### `setuptools_scm.version_scheme` (`semver`)

The `semver` version scheme formats clean (no commits or unstaged changes since last tag) versions
as the last tag, verbatim. If there *are* commits or unstaged changes, the behaviour depends on the
last tag:

- If the last tag is a pre-release, then an ISO 8601 date and time will be added as an extra
  pre-release segment. If there are no unstaged changes, the commit time of the current `HEAD` will
  be used. If there are unstaged changes, the current time will be used (hence note that unstaged
  changes will cause different versions to be generated every time).

  **Examples**

  Given a latest tag of `1.2.3-rc.1`, and no unstaged changes with a last commit time of 18:17:00
  UTC on 27th September 2019, the version scheme result would be:

  ```
  1.2.3-rc.1.20190927T181700Z
  ```

  If there were unstaged changes, and the current time was 15:49:32 BST on 8th October 2019, the
  version scheme result would be:

  ```
  1.2.3-rc.1.20191008T144932Z
  ```

- If the last tag is *not* a pre-release, the 'patch' number of the last tag is bumped and an ISO
  8601 date and time is added as a pre-release segment, as above.

  **Examples**

  Given a latest tag of `1.2.3`, and no unstaged changes with a last commit time of 18:17:00 UTC on
  27th September 2019, the version scheme result would be:

  ```
  1.2.4-20190927T181700Z
  ```

  If there were unstaged changes, and the current time was 15:49:32 BST on 8th October 2019, the
  version scheme result would be:

  ```
  1.2.4-20191008T144932Z
  ```

These choices ensure that versions generated from newer commits (or at a later time, when there are
unstaged changes) will be sorted higher than versions from older commits (or earlier times).

#### `setuptools_scm.local_scheme` (`semver`)

The `semver` local scheme does nothing when there are no commits since the last tag. When there are,
it returns a build metadata segment with a short hash for the latest commit.

**Example**

Given there are commits since the last tag and the latest commit's hash is
`ddb8be7ecb639fe0d5f72aeb46fe0b86eb77d00d`, the local scheme result would be:

```
+ddb8be7
```

Per the spec, build metadata has no effect on ordering so this is for additional context only.

### Functions

#### `git.parse`

Constructs a `setuptools_scm.version.ScmVersion` from a given `root` directory and `config`, parsing
and storing the discovered git tag using [`semver.VersionInfo`].

This behaves very similarly to to `setuptools_scm.git.parse` except that it also prevents
`setuptools_scm` from parsing the tag using [`pkg_resources.parse_version`], since that results in
[PEP 440] versions that are not SemVer-compatible.

#### `get_version`

A trivial wrapper around `setuptools_scm.get_version` that sets the `parse`, `version_scheme`, and
`local_scheme` configuration to the implementations in this package. The the `setuptools_scm`
[configuration documentation] for all options.

[SemVer]: https://semver.org
[`setuptools_scm`]: https://github.com/pypa/setuptools_scm
[PEP 440]: https://www.python.org/dev/peps/pep-0440/#version-scheme
[pip]: https://pip.pypa.io/en/stable/
[`parse`]: #gitparse
[`version_scheme`]: #setuptools_scmversion_scheme-semver
[`local_scheme`]: #setuptools_scmlocal_scheme-semver
[`get_version`]: #get_version
[configuration documentation]: https://github.com/pypa/setuptools_scm/#configuration-parameters
[`semver.VersionInfo`]: https://python-semver.readthedocs.io/en/latest/api.html#semver.VersionInfo
[`pkg_resources.parse_version`]: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#parsing-utilities
