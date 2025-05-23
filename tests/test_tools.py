import pytest
from mediawiki_agent.tools import GetPageContentTool

def test_get_page_content_tool(mocker):
    # 1. Mock pywikibot.Site
    mock_site_instance = mocker.MagicMock()
    mock_site_constructor = mocker.patch('pywikibot.Site', return_value=mock_site_instance)

    # 2. Mock pywikibot.Page
    mock_page_instance = mocker.MagicMock()
    mock_page_instance.text = "This is the page content."
    mock_page_constructor = mocker.patch('pywikibot.Page', return_value=mock_page_instance)

    # 3. Instantiate the tool
    site_url = "https://test.wikipedia.org/w/api.php"
    tool = GetPageContentTool(site_url=site_url)

    # 4. Call the run method
    page_title = "Test Page"
    result = tool.run(page_title)

    # 5. Assertions
    mock_site_constructor.assert_called_once_with(url=site_url)
    mock_page_constructor.assert_called_once_with(mock_site_instance, page_title)
    assert result == "This is the page content."
