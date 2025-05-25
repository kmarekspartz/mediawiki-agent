from mediawiki_agent.tools import get_page_content


def test_get_page_content_tool(mocker):
    # 1. Mock pywikibot.Site
    mock_site_instance = mocker.MagicMock()

    # 2. Mock pywikibot.Page
    mock_page_instance = mocker.MagicMock()
    mock_page_instance.text = "This is the page content."
    mock_page_constructor = mocker.patch(
        "pywikibot.Page", return_value=mock_page_instance
    )

    # 3. Instantiate the tool
    result = get_page_content(site=mock_site_instance, page_title = "Test Page")

    # 5. Assertions
    mock_page_constructor.assert_called_once_with(mock_site_instance, page_title)
    assert result == "This is the page content."
