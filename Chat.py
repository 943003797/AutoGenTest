# 古诗词文案生成助手
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

# def get_model_client_ollama() -> OpenAIChatCompletionClient:
#     return OpenAIChatCompletionClient(
#         model="llama3.2:latest",
#         api_key="NULL",
#         base_url="http://localhost:11434/v1",
#         model_capabilities={
#             "json_output": True,
#             "vision": False,
#             "function_calling": True,
#         },
#     )
# local_llama = get_model_client_ollama()

gpt_4o = OpenAIChatCompletionClient(
    model="gpt-4o-mini-2024-07-18",
    api_key="sk-g7GQFlpo56EY7XiopY34k4qJxOBzftAYTzTofeaGoCFvTK5I",
    base_url="https://yunwu.ai/v1"
    )

deepseek = OpenAIChatCompletionClient(
    model="deepseek-chat",
    api_key="sk-88153123bd974b9c9e8dc02eeaf5ffc4",
    base_url="https://api.deepseek.com"
    )

deepseek_searching = OpenAIChatCompletionClient(
    model="deepseek-r1-searching",
    api_key="sk-88153123bd974b9c9e8dc02eeaf5ffc4",
    base_url="https://api.deepseek.com"
    )

async def main() -> None:


    agent1 = AssistantAgent(
        name="deepseek",
        model_client=deepseek,
        system_message="你在参加一场辩论，你需要用你的逻辑，证明chatgpt很差劲，用贴吧风格，每轮对话不能超过50字。",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent2 = AssistantAgent(
        name="gpt_4o",
        model_client=gpt_4o,
        system_message="你在参加一场辩论，你需要用你的逻辑，证明deepseek很差劲，每轮对话不能超过50字。",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(20)
    termination = text_termination | max_message_termination
    reflection_team = RoundRobinGroupChat(participants=[agent1,agent2], termination_condition=termination, max_turns=None)
    
    stream = reflection_team.run_stream(task="开始辩论")
    await Console(stream)

asyncio.run(main())