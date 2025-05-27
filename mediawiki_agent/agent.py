from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from mediawiki_agent.tools import get_page_content, add_text, check_weblinks


llm = ChatOpenAI(
    model="phi-4",
    base_url="http://127.0.0.1:1234/v1",
    api_key=SecretStr("na"),
    temperature=0,
)

tools = [get_page_content, add_text, check_weblinks]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that can interact with MediaWiki pages.",
        ),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    question = "What are some themes from the Todo page on the wiki?"
    print(f"Asking: {question}")
    response = agent_executor.invoke({"input": question})
    print(f"Response: {response}")
