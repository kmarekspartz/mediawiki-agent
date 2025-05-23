# mediawiki-agent

[Smolagents](https://smolagents.org) components to interact with [pywikibot](https://pypi.org/project/pywikibot/).

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install smolagents pywikibot
```

## Usage

### GetPageContentTool

The `GetPageContentTool` can be used to fetch the content of a page from a MediaWiki site, such as Wikipedia.

Here's an example of how to use it:

```python
from mediawiki_agent.tools.get_page_content_tool import GetPageContentTool

# Instantiate the tool for Wikipedia
# Or replace with your own MediaWiki site URL
tool = GetPageContentTool(site_url="https://en.wikipedia.org/w/api.php")

# Get the content of a page
page_title = "Python (programming language)"
content = tool.run(page_title)

# Print the fetched content
print(content)
```

## Development

### Formatting and Linting

This project uses `ruff` for formatting and linting.

To install `ruff`, run:

```bash
pip install .[lint]
```

To format and lint the code, run:

```bash
ruff format . && ruff check .
```
