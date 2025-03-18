# 古诗词文案生成助手
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


deepseek=OpenAIChatCompletionClient(model="gpt-4o")

async def main():
    # 将await操作移到异步函数内部
    fetch_mcp_server = StdioServerParams(command="node", args=["C:\\Users\\Kinso\\Documents\\Cline\\MCP\\fetch-mcp\\dist\\index.js"])
    tools_fetch = await mcp_server_tools(fetch_mcp_server)
    
    agent1 = AssistantAgent(
            name="agent1",
            model_client=deepseek,
            tools=tools_fetch,
            system_message="你是一个网页信息整理员,根据给定的url,提炼内容"
        )

    agent2 = AssistantAgent(
            name="agent2",
            model_client=deepseek,
            system_message="你是一个文案编辑，会依据跟定的内容，润色成短视频文案"
        )

    agent3 = AssistantAgent(
            name="agent3",
            model_client=deepseek,
            system_message="你是一个文案审核员，会依据跟定的文案内容，审核文案是否涉及敏感信息，如果没问题，回复：Pass"
        )

    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(5)
    termination = text_termination | max_message_termination

    reflection_team = RoundRobinGroupChat(participants=[agent1], termination_condition=termination, max_turns=None)
    stream = reflection_team.run_stream(task="https://943003797.github.io/python/env")
    
    # 使用Console显示结果
    await Console(stream)

# 运行异步函数
asyncio.run(main())
