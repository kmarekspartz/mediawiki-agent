from unittest.mock import MagicMock # Keep MagicMock from unittest.mock

import requests  # For requests.exceptions.RequestException

from mediawiki_agent.tools import get_page_content, add_text, check_weblinks


# Existing test - keep it as is
def test_get_page_content_tool(mocker):  # mocker is from pytest-mock
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


class TestAddText:
    def test_add_text_bottom(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        mock_site_instance = MockSite.return_value
        mock_page_instance = MockPage.return_value
        mock_page_instance.text = "Existing content"

        page_title = "Test Page"
        text_to_add = " New text"
        summary = "Test summary bottom"

        add_text(page_title, text_to_add, summary, position="bottom")

        MockSite.assert_called_once()
        MockPage.assert_called_once_with(mock_site_instance, page_title)
        assert mock_page_instance.text == "Existing content New text"
        mock_page_instance.save.assert_called_once_with(summary)

    def test_add_text_top(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        mock_site_instance = MockSite.return_value
        mock_page_instance = MockPage.return_value
        mock_page_instance.text = "Existing content"

        page_title = "Test Page"
        text_to_add = "New text "
        summary = "Test summary top"

        add_text(page_title, text_to_add, summary, position="top")

        MockSite.assert_called_once()
        MockPage.assert_called_once_with(mock_site_instance, page_title)
        assert mock_page_instance.text == "New text Existing content"
        mock_page_instance.save.assert_called_once_with(summary)

    def test_add_text_empty_page_bottom(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value
        mock_page_instance.text = ""

        page_title = "Empty Page"
        text_to_add = "Some text"
        summary = "Test summary empty bottom"

        add_text(page_title, text_to_add, summary, position="bottom")

        assert mock_page_instance.text == "Some text"
        mock_page_instance.save.assert_called_once_with(summary)

    def test_add_text_empty_page_top(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value
        mock_page_instance.text = ""

        page_title = "Empty Page"
        text_to_add = "Some text"
        summary = "Test summary empty top"

        add_text(page_title, text_to_add, summary, position="top")

        assert mock_page_instance.text == "Some text"
        mock_page_instance.save.assert_called_once_with(summary)


class TestCheckWeblinks:
    def test_check_weblinks_no_broken_links(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
        mock_site_instance = (
            MockSite.return_value
        )  # Used in MockPage.assert_called_once_with
        mock_page_instance = MockPage.return_value

        urls = ["http://example.com/working"]
        mock_page_instance.extlinks.return_value = urls

        mock_response = MagicMock()
        mock_response.status_code = 200
        MockRequestsGet.return_value = mock_response

        page_title = "Test Page"
        result = check_weblinks(page_title)

        MockSite.assert_called_once()
        MockPage.assert_called_once_with(mock_site_instance, page_title)
        MockRequestsGet.assert_called_once_with(urls[0], timeout=10)
        assert result == []

    def test_check_weblinks_one_broken_link_status_code(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value

        urls = ["http://example.com/broken"]
        mock_page_instance.extlinks.return_value = urls

        mock_response = MagicMock()
        mock_response.status_code = 404
        MockRequestsGet.return_value = mock_response

        page_title = "Test Page"
        result = check_weblinks(page_title)

        assert result == ["http://example.com/broken"]
        MockRequestsGet.assert_called_once_with(urls[0], timeout=10)

    def test_check_weblinks_one_broken_link_exception(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value

        urls = ["http://example.com/timeout"]
        mock_page_instance.extlinks.return_value = urls

        MockRequestsGet.side_effect = requests.exceptions.RequestException

        page_title = "Test Page"
        result = check_weblinks(page_title)

        assert result == ["http://example.com/timeout"]
        MockRequestsGet.assert_called_once_with(urls[0], timeout=10)

    def test_check_weblinks_mixed_links(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value

        urls = [
            "http://example.com/working",
            "http://example.com/broken404",
            "http://example.com/broken_timeout",
        ]
        mock_page_instance.extlinks.return_value = urls

        def side_effect_func(url, timeout):
            if url == "http://example.com/working":
                response = MagicMock()
                response.status_code = 200
                return response
            elif url == "http://example.com/broken404":
                response = MagicMock()
                response.status_code = 404
                return response
            elif url == "http://example.com/broken_timeout":
                raise requests.exceptions.RequestException
            return MagicMock()  # Should not happen

        MockRequestsGet.side_effect = side_effect_func

        page_title = "Test Page"
        result = check_weblinks(page_title)

        assert result == [
            "http://example.com/broken404",
            "http://example.com/broken_timeout",
        ]
        assert MockRequestsGet.call_count == 3

    def test_check_weblinks_no_external_links(self, mocker):
        MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
        MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
        MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
        MockSite()  # Ensures Site() is called
        mock_page_instance = MockPage.return_value
        mock_page_instance.extlinks.return_value = []

        page_title = "Test Page"
        result = check_weblinks(page_title)

        assert result == []
        MockRequestsGet.assert_not_called()
