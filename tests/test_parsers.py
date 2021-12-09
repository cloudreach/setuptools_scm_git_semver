import pytest

from setuptools_scm_git_semver import parse_version_txt


@pytest.fixture
def Path(mocker):
    return mocker.patch("setuptools_scm_git_semver.Path", autospec=True)


class TestParseVersionTxt:
    def test_when_a_version_file_exists__its_content_is_returned_as_the_version(
        self, Path, faker
    ):
        root = faker.word()
        config = object()
        version_txt_path = Path(root) / "VERSION.txt"

        parsed = parse_version_txt(root, config)

        assert parsed.tag is version_txt_path.read_text.return_value
        assert parsed.preformatted
        assert parsed.config is config
