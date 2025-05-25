import pywikibot
import requests
from smolagents import tool
from typing import Any, List


@tool
def get_page_content(page_title: str) -> Any:  # str
    """
    Gets the content of a MediaWiki page using a pywikibot Site.

    Args:
        site: a pywikibot.Site.
        page_title: a string with the page title/path to the page within the Wiki.

    Returns:
        A string with the text content of the MediaWiki page
    """
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)
    return page.text


@tool
def add_text(
    page_title: str, text_to_add: str, summary: str, position: str = "bottom"
) -> None:
    """
    Adds text to a MediaWiki page, either at the top or bottom.

    Args:
        page_title: The title of the MediaWiki page.
        text_to_add: The text to add to the page.
        summary: The summary of the edit.
        position: Where to add the text, either 'top' or 'bottom'. Defaults to 'bottom'.
    """
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)

    if position == "top":
        page.text = text_to_add + page.text
    elif position == "bottom":
        page.text = page.text + text_to_add
    else:
        raise ValueError("Position must be either 'top' or 'bottom'")

    page.save(summary)


@tool
def check_weblinks(page_title: str) -> List[str]:
    """
    Checks all external links on a MediaWiki page for 4xx or 5xx HTTP status codes.

    Args:
        page_title: The title of the MediaWiki page.

    Returns:
        A list of URLs that are broken.
    """
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)
    broken_links: List[str] = []

    for link in page.extlinks():
        try:
            response = requests.get(link, timeout=10)  # Added timeout
            if response.status_code >= 400:
                broken_links.append(link)
        except requests.exceptions.RequestException:
            # Includes ConnectionError, Timeout, TooManyRedirects, etc.
            broken_links.append(link)

    return broken_links
