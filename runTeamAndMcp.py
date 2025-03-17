import os
import asyncio
import config
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools


# 将agent初始化移动到异步函数中
async def main():

    deepseek=OpenAIChatCompletionClient(model="deepseek-chat")

    fetch_mcp_server = StdioServerParams(command="node", args=["mcp/fetch-mcp/dist/index.js"])

    tools_fetch = await mcp_server_tools(fetch_mcp_server)
    
    # 定义agent1时传入初始化后的工具
    agent1 = AssistantAgent(  # 修复缩进
        name="agent1",
        model_client=deepseek,
        tools=tools_fetch,
        system_message="你是网页内容获取助手，使用你的fetch工具，获取给定url的网页内容"
    )

    agent2 = AssistantAgent(  # 修复缩进
        name="agent2",
        model_client=deepseek,
        system_message="你是一个微信公众号文章写手，会依据跟定的内容，写出微信公众号风格的微信公众号文章，包括标题，正文，结尾，字数在200字左右"
    )

    agent3 = AssistantAgent(  # 修复缩进
        name="agent3",
        model_client=deepseek,
        system_message="你是一个文章审核员，会依据跟定的文章内容，审核文章是否涉及敏感信息，如果没问题，回复：Pass"
    )

    # 以下代码需要移到main函数内部
    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(2)
    termination = text_termination | max_message_termination
    reflection_team = RoundRobinGroupChat(participants=[agent1], termination_condition=termination, max_turns=None)
    
    stream = reflection_team.run_stream(task="https://943003797.github.io/python/env/")
    await Console(stream)  # 修复缩进

# 运行异步函数
asyncio.run(main())
