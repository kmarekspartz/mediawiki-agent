from unittest.mock import patch, MagicMock
import pytest
from mediawiki_agent.agent import agent_executor # The AgentExecutor instance
# To mock the tool function directly if it's easier than mocking pywikibot calls within it for this test
from mediawiki_agent.tools import get_page_content as get_page_content_tool_function
from langchain_core.messages import AIMessage


@patch('mediawiki_agent.tools.get_page_content', name='mock_get_page_content_tool_func') # Mock the actual tool function in tools.py
@patch('mediawiki_agent.agent.ChatOpenAI', name='MockChatOpenAI') # Mock the LLM class in agent.py
def test_langchain_agent_uses_get_page_content(MockChatOpenAI, mock_get_page_content_tool_func):
    # Configure the mock LLM instance
    mock_llm_instance = MagicMock()
    MockChatOpenAI.return_value = mock_llm_instance

    # Simulate the LLM deciding to call get_page_content and then providing a final answer
    llm_decision_tool_call = AIMessage(
        content="",  # OpenAI Functions agent often has empty content when making a tool call
        additional_kwargs={
            "tool_calls": [{
                "id": "call_abc123",  # ID can be arbitrary for the mock
                "function": {
                    "name": "get_page_content",
                    "arguments": '{"page_title":"Test Page"}' # Arguments as a JSON string
                }
            }]
        }
    )
    llm_final_answer = AIMessage(content="The content of Test Page is: Mocked page content here.")
    mock_llm_instance.invoke.side_effect = [llm_decision_tool_call, llm_final_answer]

    # Configure the mock for the get_page_content tool function
    mock_get_page_content_tool_func.return_value = "Mocked page content here."

    # Invoke the agent_executor
    input_prompt = "What is the content of Test Page?"
    # The agent_executor is imported from mediawiki_agent.agent
    response = agent_executor.invoke({"input": input_prompt})

    # Add assertions
    # Check that the mock LLM was called (expected twice: once for tool decision, once for final answer)
    assert mock_llm_instance.invoke.call_count == 2

    # Check that the get_page_content tool function was called with the correct arguments
    mock_get_page_content_tool_func.assert_called_once_with(page_title="Test Page")

    # Check the final response from the agent
    assert response is not None
    assert "output" in response, "The response dictionary should have an 'output' key."
    assert response["output"] == "The content of Test Page is: Mocked page content here."


@pytest.mark.skip(reason="Feature not yet implemented")
def test_access_page_history_placeholder():
    pass


@pytest.mark.skip(reason="Feature not yet implemented")
def test_site_information_placeholder():
    pass
