from mediawiki_agent.tools import add_text


# Tests for add_text functionality
def test_add_text_bottom(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    mock_site_instance = MockSite.return_value
    mock_page_instance = MockPage.return_value
    mock_page_instance.text = "Existing content"

    page_title = "Test Page"
    text_to_add = " New text"
    summary = "Test summary bottom"
    position = "bottom"

    add_text.run({
        "page_title": page_title,
        "text_to_add": text_to_add,
        "summary": summary,
        "position": position
    })

    MockSite.assert_called_once()
    MockPage.assert_called_once_with(mock_site_instance, page_title)

    assert mock_page_instance.text == "Existing content New text"
    mock_page_instance.save.assert_called_once_with(summary)


def test_add_text_top(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    mock_site_instance = MockSite.return_value
    mock_page_instance = MockPage.return_value
    mock_page_instance.text = "Existing content"

    page_title = "Test Page"
    text_to_add = "New text "
    summary = "Test summary top"
    position = "top"

    add_text.run({
        "page_title": page_title,
        "text_to_add": text_to_add,
        "summary": summary,
        "position": position
    })

    MockSite.assert_called_once()
    MockPage.assert_called_once_with(mock_site_instance, page_title)
    assert mock_page_instance.text == "New text Existing content"
    mock_page_instance.save.assert_called_once_with(summary)


def test_add_text_empty_page_bottom(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockSite()
    mock_page_instance = MockPage.return_value
    mock_page_instance.text = ""

    page_title = "Empty Page"
    text_to_add = "Some text"
    summary = "Test summary empty bottom"
    position = "bottom"

    add_text.run({
        "page_title": page_title,
        "text_to_add": text_to_add,
        "summary": summary,
        "position": position
    })

    assert mock_page_instance.text == "Some text"
    mock_page_instance.save.assert_called_once_with(summary)


def test_add_text_empty_page_top(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockSite()
    mock_page_instance = MockPage.return_value
    mock_page_instance.text = ""

    page_title = "Empty Page"
    text_to_add = "Some text"
    summary = "Test summary empty top"
    position = "top"

    add_text.run({
        "page_title": page_title,
        "text_to_add": text_to_add,
        "summary": summary,
        "position": position
    })

    assert mock_page_instance.text == "Some text"
    mock_page_instance.save.assert_called_once_with(summary)
