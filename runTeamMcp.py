# 古诗词文案生成助手
import os
import asyncio
import config
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools


deepseek=OpenAIChatCompletionClient(model="deepseek-chat",)
ollama_model_client = OllamaChatCompletionClient(model="llama3:latest")
def get_model_client_ollama() -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model="llama3.2:latest",
        api_key="NULL",
        base_url="http://localhost:11434/v1",
        model_capabilities={
            "json_output": True,
            "vision": False,
            "function_calling": True,
        },
    )
local_llama = get_model_client_ollama()

async def main():
    # 将await操作移到异步函数内部
    fetch_mcp_server = StdioServerParams(command="node", args=["mcp/fetch-mcp/dist/index.js"])
    tools_fetch = await mcp_server_tools(fetch_mcp_server)
    
    agent1 = AssistantAgent(
            name="agent1",
            model_client=local_llama,
            tools=tools_fetch,
            system_message="这个链接是一个网页，你需要获取网页主体内容"
        )

    agent2 = AssistantAgent(
            name="agent2",
            model_client=deepseek,
            system_message="你会依据跟定的HTML源代码，提炼该页面的主要内容，200字左右"
        )

    agent3 = AssistantAgent(
            name="agent3",
            model_client=deepseek,
            system_message="你是一个审核员，会依据跟定的内容，审核文案是否涉及敏感信息，如果没问题，回复：Pass"
        )

    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(5)
    termination = text_termination | max_message_termination

    reflection_team = RoundRobinGroupChat(participants=[agent1,agent2], termination_condition=termination, max_turns=None)
    stream = reflection_team.run_stream(task="https://baike.so.com/doc/5343102-5578545.html")
    
    # 使用Console显示结果
    await Console(stream)

# 运行异步函数
asyncio.run(main())
