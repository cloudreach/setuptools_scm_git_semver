import pytest
from freezegun import freeze_time
from setuptools_scm import get_version


def no_version(*args):
    return ""


class TestIntegrationWithSetuptoolsScm:
    @pytest.mark.parametrize(
        "versions",
        (
            ("0.1.2-0-g0123456789ab", "0.1.2"),
            ("0.1.2-1-g0123456789ab", "0.1.3-rc.0"),
            ("0.1.2-0-g0123456789ab-dirty", "0.1.3-rc.0"),
            ("0.1.2-1-g0123456789ab-dirty", "0.1.3-rc.0"),
        ),
    )
    def test_get_next_rc_after_release_tag(self, versions):
        tag, current_version = versions
        assert (
            get_version(
                version_scheme="guess-next-rc",
                local_scheme=no_version,
                git_describe_command=f"echo {tag}",
            )
            == current_version
        )

    @pytest.mark.parametrize(
        "versions",
        (
            ("0.1.2-rc.3-0-g0123456789ab", "0.1.2-rc.3"),
            ("0.1.2-rc.3-1-g0123456789ab", "0.1.2-rc.4"),
            ("0.1.2-rc.3-0-g0123456789ab-dirty", "0.1.2-rc.4"),
            ("0.1.2-rc.3-1-g0123456789ab-dirty", "0.1.2-rc.4"),
        ),
    )
    def test_get_next_rc_after_rc_tag(self, versions):
        tag, current_version = versions
        assert (
            get_version(
                version_scheme="guess-next-rc",
                local_scheme=no_version,
                git_describe_command=f"echo {tag}",
                normalize=False,
            )
            == current_version
        )

    @pytest.mark.parametrize(
        "versions",
        (
            ("0.1.2-0-g0123456789ab", ""),
            ("0.1.2-1-g0123456789ab", "+20200220t202202z.g0123456789ab"),
            ("0.1.2-0-g0123456789ab-dirty", "+20200220t202202z.g0123456789ab"),
            ("0.1.2-1-g0123456789ab-dirty", "+20200220t202202z.g0123456789ab"),
        ),
    )
    @freeze_time("2020-02-20T20:22:02Z")
    def test_get_time_dot_node_version(self, versions):
        tag, current_version = versions
        assert (
            get_version(
                version_scheme=no_version,
                local_scheme="time-dot-node",
                git_describe_command=f"echo {tag}",
            )
            == current_version
        )
