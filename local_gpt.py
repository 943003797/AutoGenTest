import nest_asyncio
nest_asyncio.apply()

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_agentchat.ui import Console

def get_model_client_ollama() -> OpenAIChatCompletionClient:  # type: ignore
    return OpenAIChatCompletionClient(
        model="chevalblanc/gpt-4o-mini:latest",
        api_key="NULL",
        base_url="http://localhost:11434/v1",
        model_capabilities={
            "json_output": False,
            "vision": False,
            "function_calling": True,
        },
    )

async def main() -> None:
    model_client = get_model_client_ollama()

    agent1 = AssistantAgent("Assistant1", model_client=model_client)
    await Console(agent1.run_stream(task="列举两条让人意难平的诗句"))

asyncio.run(main())