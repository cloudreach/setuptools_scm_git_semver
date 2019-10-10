from datetime import datetime
import subprocess

import dateutil.parser
import semver
from setuptools_scm import get_version as setuptools_scm_version

from .git import parse


COMMIT_TIME_ARGS = ['git', 'show', '--pretty=%cI', '-s']
TIME_FORMAT = '%Y%m%dT%H%M%SZ'


def get_version(**kwargs):
    return setuptools_scm_version(parse=parse,
                                  version_scheme='semver',
                                  local_scheme='semver',
                                  **kwargs)


def version_scheme_semver(version):
    tag = version.tag

    if not version.distance and not version.dirty:
        return str(tag)

    version.time = datetime.now() if version.dirty else _get_commit_time()
    base = f'{tag}.' if tag.prerelease else f'{semver.bump_patch(str(tag))}-'
    return version.format_with('{base}{time:{time_format}}', base=base, time_format=TIME_FORMAT)


def local_scheme_semver(version):
    if version.distance and version.node:
        return f'+{version.node[1:]}'
    return ''


def _get_commit_time():
    try:
        commit_time = subprocess.check_output(COMMIT_TIME_ARGS, stderr=subprocess.DEVNULL).strip()
        return dateutil.parser.isoparse(commit_time)
    except Exception:
        # This could happen, e.g., if there are no commits in the repo. We assume other git issues
        # would break before this point and assume that case for the sake of simple error handling.
        return datetime.now()
