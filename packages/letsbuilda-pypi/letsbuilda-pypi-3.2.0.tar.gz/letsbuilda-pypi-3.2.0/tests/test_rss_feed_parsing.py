"""Test parsing metadata from the RSS feeds"""

from datetime import datetime

from letsbuilda.pypi import RSSPackageMetadata


def test_parse_publication_date() -> None:
    """Confirm publication date gets parsed correctly"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "description": "a test package",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = RSSPackageMetadata.build_from(data)
    assert parsed_data.publication_date == datetime(2023, 3, 29, 21, 30, 5)


def test_author_missing() -> None:
    """Confirm missing author gets set to None"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "description": "a test package",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = RSSPackageMetadata.build_from(data)
    assert parsed_data.author is None


def test_description_missing() -> None:
    """Confirm missing description gets set to None"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = RSSPackageMetadata.build_from(data)
    assert parsed_data.description is None


def test_new_package_has_no_version() -> None:
    """Parse the lack of version from the new packages feed"""
    data = {
        "title": "test-package added to PyPI",
        "link": "https://pypi.org/project/test-package",
        "guid": "https://pypi.org/project/test-package",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = RSSPackageMetadata.build_from(data)
    assert parsed_data.version is None


def test_update_package_has_version() -> None:
    """Parse the version from the updated packages feed"""
    data = {
        "title": "test-package 1.0.0",
        "link": "https://pypi.org/project/test-package/1.0.0",
        "author": "test-author@example.com",
        "pubDate": "Wed, 29 Mar 2023 21:30:05 GMT",
    }
    parsed_data = RSSPackageMetadata.build_from(data)
    assert parsed_data.version == "1.0.0"
