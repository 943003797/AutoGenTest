import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.base import TaskResult

os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"
os.environ["OPENAI_API_KEY"] = "sk-88153123bd974b9c9e8dc02eeaf5ffc4"

# Define a simple function tool that the agent can use.
# For this example, we use a fake weather tool for demonstration purposes.
async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 73 degrees and Sunny."

# Define an AssistantAgent with the model, tool, system message, and reflection enabled.
# The system message instructs the agent via natural language.
model_client=OpenAIChatCompletionClient(
            model="deepseek-chat",
            # api_key="sk-88153123bd974b9c9e8dc02eeaf5ffc4",
            # base_url="https://api.wlai.vip/v1"
        )
local_gpt = OllamaChatCompletionClient(
    model="gpt-4o-mini",
    base_url="http://127.0.0.1:11434",
    context_window=128000,  # 添加必要参数
    max_tokens=4096
)
agent = AssistantAgent(
    name="weather_agent",
    model_client=local_gpt,
    system_message="你是个乐于助人的助手。使用中文回复用户。",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)

# Run the agent and stream the messages to the console.
async def main() -> None:
    await Console(agent.run_stream(task="列举两条让人意难平的诗句"))

async def run_main():
    await main()

asyncio.run(run_main())