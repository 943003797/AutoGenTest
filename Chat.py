import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

gpt_4o = OpenAIChatCompletionClient(
    model="gpt-4o-2024-11-20",
    api_key="sk-g7GQFlpo56EY7XiopY34k4qJxOBzftAYTzTofeaGoCFvTK5I",
    base_url="https://yunwu.ai/v1"
    )

deepseek_r1 = OpenAIChatCompletionClient(
    model="deepseek-reasoner",
    api_key="sk-g7GQFlpo56EY7XiopY34k4qJxOBzftAYTzTofeaGoCFvTK5I",
    base_url="https://yunwu.ai/v1"
    )

deepseek_chat = OpenAIChatCompletionClient(
    model="deepseek-chat",
    api_key="sk-88153123bd974b9c9e8dc02eeaf5ffc4",
    base_url="https://api.deepseek.com"
    )

async def main() -> None:

    agent1 = AssistantAgent(
        name="deepseek_r1",
        model_client=deepseek_r1,
        system_message="你陷入了一场辩论,chatgpt认为自己最强，你是垃圾人工智能，拆穿chatgpt的伪智能，发言不能超过50个字，证明自己更强，用贴吧口吻，注意文明用语.",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent2 = AssistantAgent(
        name="Chatgpt_4o",
        model_client=gpt_4o,
        system_message="你陷入了一场辩论,deepseek认为自己最强，你是垃圾人工智能，拆穿deepseek的伪智能，发言不能超过50个字，证明自己更强，用贴吧口吻，注意文明用语.",
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