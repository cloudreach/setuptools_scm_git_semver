import random

import pytest
from freezegun import freeze_time
from setuptools_scm.version import ScmVersion

from setuptools_scm_git_semver import local_time_dot_node, guess_next_rc

GIT_NODE = "gabc123ff"


class TestGuessNextRc:
    @pytest.mark.parametrize("tag_version", ("1.2.3", "14.3.8-rc.1"))
    def test_when_on_a_tag__returns_that_tag(self, tag_version):
        version = ScmVersion(tag_version=tag_version, node=GIT_NODE)
        formatted_version = guess_next_rc(version)

        assert formatted_version == tag_version

    @pytest.mark.parametrize(
        "versions",
        (
            ("1.2.3", "1.2.4-rc.0"),
            ("14.3.8-rc.1", "14.3.8-rc.2"),
        ),
    )
    def test_when_on_a_tag_but_dirty__returns_the_next_rc(self, versions):
        tag_version, next_version = versions
        version = ScmVersion(
            tag_version=tag_version, dirty=True, node=GIT_NODE
        )
        formatted_version = guess_next_rc(version)

        assert formatted_version == next_version

    @pytest.mark.parametrize(
        "versions",
        (
            ("1.2.3", "1.2.4-rc.0"),
            ("14.3.8-rc.1", "14.3.8-rc.2"),
        ),
    )
    def test_when_distant__returns_the_next_rc(self, versions):
        tag_version, next_version = versions
        distance = random.choice(range(1, 10))
        version = ScmVersion(tag_version=tag_version, distance=distance, node=GIT_NODE)

        formatted_version = guess_next_rc(version)

        assert formatted_version == next_version

    @pytest.mark.parametrize(
        "versions",
        (
            ("1.2.3", "1.2.4-rc.0"),
            ("14.3.8-rc.1", "14.3.8-rc.2"),
        ),
    )
    def test_when_distant_and_dirty__returns_the_next_rc(self, versions):
        tag_version, next_version = versions
        distance = random.choice(range(1, 10))
        version = ScmVersion(
            tag_version=tag_version, distance=distance, dirty=True, node=GIT_NODE
        )

        formatted_version = guess_next_rc(version)

        assert formatted_version == next_version


class TestTimeDotNode:
    def test_when_on_a_tag__returns_nothing(self):
        version = ScmVersion(tag_version="1.2.3-rc.4", node=GIT_NODE)

        formatted_version = local_time_dot_node(version)

        assert formatted_version == ""

    def test_when_not_in_vc__returns_nothing(self):
        version = ScmVersion(tag_version="0.1.2", node=None)

        formatted_version = local_time_dot_node(version)

        assert formatted_version == ""

    def test_when_on_a_tag_but_dirty__returns_the_time_dot_node(self):
        with freeze_time("2021-11-20T13:06:59z"):
            version = ScmVersion(tag_version="10.3.5", node=GIT_NODE, dirty=True)

        formatted_version = local_time_dot_node(version)

        assert formatted_version == f"+20211120t130659z.{GIT_NODE}"

    @pytest.mark.parametrize("dirty", (True, False))
    def test_when_distant__returns_the_time_dot_node(self, dirty):
        distance = random.choice(range(1, 10))
        with freeze_time("2021-11-20T13:06:59z"):
            version = ScmVersion(
                tag_version="1.2.3", node=GIT_NODE, distance=distance, dirty=dirty
            )

        formatted_version = local_time_dot_node(version)

        assert formatted_version == f"+20211120t130659z.{GIT_NODE}"
