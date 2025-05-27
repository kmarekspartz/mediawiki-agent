import requests  # For requests.exceptions.RequestException
from mediawiki_agent.tools import check_weblinks


# Tests for check_weblinks functionality (extracted from TestCheckWeblinks class)
def test_check_weblinks_no_broken_links(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
    mock_site_instance = MockSite.return_value
    mock_page_instance = MockPage.return_value

    urls = ["http://example.com/working"]
    mock_page_instance.extlinks.return_value = urls

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    MockRequestsGet.return_value = mock_response

    page_title = "Test Page"
    result = check_weblinks.run({"page_title": page_title})

    MockSite.assert_called_once()
    MockPage.assert_called_once_with(mock_site_instance, page_title)
    MockRequestsGet.assert_called_once_with(urls[0], timeout=10)

    assert result == []


def test_check_weblinks_one_broken_link_status_code(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
    MockSite()
    mock_page_instance = MockPage.return_value

    urls = ["http://example.com/broken"]
    mock_page_instance.extlinks.return_value = urls

    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    MockRequestsGet.return_value = mock_response

    page_title = "Test Page"
    result = check_weblinks.run({"page_title": page_title})

    assert result == ["http://example.com/broken"]
    MockRequestsGet.assert_called_once_with(urls[0], timeout=10)


def test_check_weblinks_one_broken_link_exception(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
    MockSite()
    mock_page_instance = MockPage.return_value

    urls = ["http://example.com/timeout"]
    mock_page_instance.extlinks.return_value = urls

    MockRequestsGet.side_effect = requests.exceptions.RequestException

    page_title = "Test Page"
    result = check_weblinks.run({"page_title": page_title})

    assert result == ["http://example.com/timeout"]
    MockRequestsGet.assert_called_once_with(urls[0], timeout=10)


def test_check_weblinks_mixed_links(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
    MockSite()
    mock_page_instance = MockPage.return_value

    urls = [
        "http://example.com/working",
        "http://example.com/broken404",
        "http://example.com/broken_timeout",
    ]
    mock_page_instance.extlinks.return_value = urls

    def side_effect_func(url, timeout):
        if url == "http://example.com/working":
            response = mocker.MagicMock()
            response.status_code = 200
            return response
        elif url == "http://example.com/broken404":
            response = mocker.MagicMock()
            response.status_code = 404
            return response
        elif url == "http://example.com/broken_timeout":
            raise requests.exceptions.RequestException
        return mocker.MagicMock()

    MockRequestsGet.side_effect = side_effect_func

    page_title = "Test Page"
    result = check_weblinks.run({"page_title": page_title})

    assert result == [
        "http://example.com/broken404",
        "http://example.com/broken_timeout",
    ]
    assert MockRequestsGet.call_count == 3


def test_check_weblinks_no_external_links(mocker):
    MockSite = mocker.patch("mediawiki_agent.tools.pywikibot.Site")
    MockPage = mocker.patch("mediawiki_agent.tools.pywikibot.Page")
    MockRequestsGet = mocker.patch("mediawiki_agent.tools.requests.get")
    MockSite()
    mock_page_instance = MockPage.return_value
    mock_page_instance.extlinks.return_value = []

    page_title = "Test Page"
    result = check_weblinks.run({"page_title": page_title})

    assert result == []
    MockRequestsGet.assert_not_called()
