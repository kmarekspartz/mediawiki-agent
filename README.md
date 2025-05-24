# MediaWiki Agent

This project provides a [Smolagents](https://smolagents.org) component designed for robust interaction with [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) sites, such as various wikis powered by MediaWiki. It leverages the comprehensive [Pywikibot](https://pypi.org/project/pywikibot/) library to offer a powerful and flexible way to automate tasks, retrieve data, and manage content on MediaWiki platforms.

The primary purpose of this agent is to enable developers and users to:
*   Programmatically access and retrieve content from MediaWiki pages.
*   Automate common wiki editing and maintenance tasks.
*   Extract and process information from wikis for analysis or other applications.
*   Integrate MediaWiki operations into larger automated workflows.

## Installation

To use this project, it's recommended to clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/kmarekspartz/mediawiki-agent.git
cd mediawiki-agent
poetry install
```

If you want to add new dependencies to the project, you can use:
```bash
poetry add <package-name>
```
The main dependencies are `smolagents` and `pywikibot`.

## Potential Usage Examples

While the agent is under development, here are some potential ways it could be used once more features are implemented:

*   **Automated Content Updates:** Imagine a scenario where you need to update a common piece of information across dozens of pages. The MediaWiki Agent could be programmed to identify these pages and apply the necessary changes automatically.
*   **Data Aggregation:** Collect information from all pages within a specific category (e.g., "Featured Articles") to compile statistics or generate reports.
*   **Change Monitoring:** Set up the agent to monitor your MediaWiki watchlist or recent changes for specific keywords, edits by certain users, or changes to important templates, and then trigger notifications or other actions.
*   **Talk Page Management:** Automate the archiving of old discussions on talk pages to keep them organized and readable.
*   **Quality Control Assistance:** While requiring careful implementation and oversight, the agent could assist in identifying and reverting common types of vandalism or unproductive edits based on predefined patterns. (Note: Automated counter-vandalism is a sensitive task and should always be used with caution and human review.)

## Core MediaWiki Interaction Features

The MediaWiki Agent is being developed to provide a comprehensive suite of tools for interacting with MediaWiki sites. These features are built upon the capabilities of the [Pywikibot](https://pypi.org/project/pywikibot/) library. Key planned and existing functionalities include:

*   **Reading Page Content:** Fetching the full content of wiki pages. (The `GetPageContentTool` described below is an initial implementation of this.)
*   **Editing Pages:** Programmatically creating new pages or modifying existing content. This includes making minor corrections, adding new sections, or overhauling articles. (The `MediaWikiAgent` class, found in `mediawiki_agent/agent.py`, includes a placeholder `edit_page` method planned for this future capability).
*   **Site Login & Authentication:** Logging into a MediaWiki site with user credentials to perform actions that require specific permissions. (The `MediaWikiAgent` class, found in `mediawiki_agent/agent.py`, includes a placeholder `login` method planned for this).
*   **Searching Pages:** Finding pages based on titles, keywords within the content, or other criteria.
*   **Working with Categories:** Listing pages within categories, adding or removing pages from categories, and creating new categories.
*   **Accessing Page History and Revisions:** Retrieving the revision history of a page, viewing specific versions, and comparing differences between revisions.
*   **Interacting with Site Information:** Querying site-level information, such as statistics, extensions installed, and user rights.
*   **(Potentially) File Uploads:** Automating the upload of images, documents, or other media to the wiki.

Further development will focus on expanding these core features and ensuring robust error handling and ease of use.

## Usage

### GetPageContentTool

The `GetPageContentTool` can be used to fetch the content of a page from any MediaWiki site.

Here's an example of how to use it:

```python
from mediawiki_agent.tools.get_page_content_tool import GetPageContentTool

# Instantiate the tool for your MediaWiki site
# Replace "https://your-mediawiki-site.org/w/api.php" with the actual API URL of your wiki.
tool = GetPageContentTool(site_url="https://your-mediawiki-site.org/w/api.php")

# Get the content of a page
# Replace "Sample Page Title" with a page title from your wiki
page_title = "Sample Page Title"
content = tool.run(page_title)

# Print the fetched content
print(content)
```

## Development

### Formatting and Linting

This project uses `ruff` for formatting and linting.

To install `ruff` and other development dependencies, run:

```bash
poetry install --with lint --with typecheck --with test 
```
(Note: the previous command `poetry install --with lint` was updated to include other dev groups as they are defined in `pyproject.toml` and it's good practice to inform how to install all of them).

To format and lint the code, run:

```bash
poetry run ruff format . && poetry run ruff check .
```
