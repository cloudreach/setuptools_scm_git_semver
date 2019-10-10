from setuptools import setup

setup(
    name='setuptools_scm_git_semver',
    use_scm_version=True,
    author='Chris Connelly',
    author_email='chris.connelly@cloudreach.com',
    description='SemVer-compatible plugin for setuptools_scm.',
    packages=['setuptools_scm_git_semver'],
    install_requires=['python-dateutil>=2.8,<3', 'semver>=2.8,<3', 'setuptools_scm>=3.3,<4'],
    setup_requires=['setuptools_scm'],
    entry_points=f"""
        [setuptools_scm.version_scheme]
        semver = setuptools_scm_git_semver:version_scheme_semver

        [setuptools_scm.local_scheme]
        semver = setuptools_scm_git_semver:local_scheme_semver
    """
)
