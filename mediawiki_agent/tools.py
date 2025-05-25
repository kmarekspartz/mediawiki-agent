import pywikibot
from smolagents import tool
from typing import Any


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
