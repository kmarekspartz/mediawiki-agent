import pywikibot
from smolagents.tools import Tool


class GetPageContentTool(Tool):
    name = "get_page_content"
    description = "Gets the content of a MediaWiki page."
    inputs = {"page_title": {"type": "string", "description": "The title of the MediaWiki page to retrieve."}}
    outputs = {"page_content": {"type": "string", "description": "The text content of the MediaWiki page."}}
    output_type = "string"

    def __init__(self, site_url):
        super().__init__()
        self.site = pywikibot.Site(url=site_url)

    def forward(self, page_title: str) -> str: # Renamed from run
        page = pywikibot.Page(self.site, page_title)
        return page.text


# Additional tools can be added similarly.
