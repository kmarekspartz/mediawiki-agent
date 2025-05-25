from smolagents import CodeAgent, OpenAIServerModel
from mediawiki_agent.tools import get_page_content


model = OpenAIServerModel(
    model_id="phi-4",
    api_base="http://127.0.0.1:1234/v1",
    api_key="na",
)


agent = CodeAgent(tools=[get_page_content], model=model, stream_outputs=True)

agent.run("What are some themes from the Todo page on the wiki?")