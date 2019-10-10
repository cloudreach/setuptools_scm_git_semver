import semver
from setuptools_scm.git import DEFAULT_DESCRIBE, GitWorkdir, _git_parse_describe, warn_on_shallow
from setuptools_scm.utils import has_command
from setuptools_scm.version import meta


def parse(root, *, config):
    """
    Based on https://github.com/pypa/setuptools_scm/blob/master/src/setuptools_scm/git.py#parse

    This is almost a verbatim copy, except that we tell setuptools_scm that the tag is preformatted
    to prevent them from applying Python's version normalisation.
    """
    if not has_command("git"):
        return

    wd = GitWorkdir.from_potential_worktree(config.absolute_root)
    if wd is None:
        return
    warn_on_shallow(wd)

    describe_command = config.git_describe_command or DEFAULT_DESCRIBE

    out, unused_err, ret = wd.do_ex(describe_command)
    if ret:
        # If 'git git_describe_command' failed, try to get the information otherwise.
        tag = '0.1.0'
        distance = wd.count_all_nodes()
        dirty = wd.is_dirty()
        node = None
        branch = None

        rev_node = wd.node()
        if rev_node is not None:
            node = f'g{rev_node}'
            branch = wd.get_branch()
    else:
        tag, distance, node, dirty = _git_parse_describe(out)
        branch = wd.get_branch()

    version = meta(
        semver.parse_version_info(tag),
        distance=distance,
        dirty=dirty,
        node=node,
        preformatted=True,
        config=config,
        branch=branch
    )
    version.preformatted = False

    return version
