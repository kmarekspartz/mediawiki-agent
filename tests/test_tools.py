# Removed: import unittest
# Removed: from unittest.mock import MagicMock

# import requests # Removed as it's no longer needed

# Only import get_page_content as add_text and check_weblinks are moved
from mediawiki_agent.tools import get_page_content


# Existing test - keep it as is (already uses mocker)
def test_get_page_content_tool(mocker):
    mock_site_instance = mocker.MagicMock()
    mocker.patch("pywikibot.Site", return_value=mock_site_instance)

    mock_page_instance = mocker.MagicMock()
    mock_page_instance.text = "This is the page content."
    mock_page_constructor = mocker.patch(
        "pywikibot.Page", return_value=mock_page_instance
    )

    page_title = "Test Page"
    result = get_page_content(page_title=page_title)

    mock_page_constructor.assert_called_once_with(mock_site_instance, page_title)
    assert result == "This is the page content."


# TestAddText class and its methods are removed
# TestCheckWeblinks class and its methods are removed
