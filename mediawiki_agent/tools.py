import pywikibot
import requests
from langchain.tools import tool
from typing import List


@tool
def get_page_content(page_title: str) -> str:
    """
    Gets the content of a MediaWiki page.

    Args:
        page_title: The title of the MediaWiki page.

    Returns:
        A string with the text content of the MediaWiki page.
    """
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)
    return page.text


@tool
def add_text(
    page_title: str, text_to_add: str, summary: str, position: str = "bottom"
) -> None:
    """Adds text to a MediaWiki page, either at the top or bottom.

    Args:
        page_title: The title of the MediaWiki page to edit.
        text_to_add: The text content to add to the page.
        summary: A brief description of the changes made.
        position: Specifies where to add the text. Must be 'top' or 'bottom'. Defaults to 'bottom'.
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
    Checks all external web links on a MediaWiki page and returns a list of broken links.
    A link is considered broken if it returns an HTTP status code of 4xx or 5xx.

    Args:
        page_title: The title of the MediaWiki page to check.

    Returns:
        A list of strings, where each string is a URL of a broken external link.
        Returns an empty list if no broken links are found or if the page has no external links.
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
