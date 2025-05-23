import pywikibot
from smolagents.tools import Tool


class GetPageContentTool(Tool):
    name = "get_page_content"
    description = "Gets the content of a MediaWiki page."

    def __init__(self, site_url):
        super().__init__()
        self.site = pywikibot.Site(url=site_url)

    def run(self, page_title: str) -> str:
        page = pywikibot.Page(self.site, page_title)
        return page.text


# Additional tools can be added similarly.
