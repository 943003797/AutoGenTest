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

async def main() -> None:

    fetch_mcp_server = await mcp_server_tools(StdioServerParams(command="python", args=["mcp/mcp_server_fetch.py"]))
    fetch_filesystem_server = StdioServerParams(
        command="npx.cmd", args=["-y", "@modelcontextprotocol/server-filesystem", "S:\\"]
    )
    tools_filesystem = await mcp_server_tools(fetch_filesystem_server)

    agent_search = AssistantAgent(
        name="agent",
        model_client=gpt_4o,
        system_message="你是一个乐于助人的AI智能助手。",
        model_client_stream=True,
        tools=fetch_mcp_server,
        reflect_on_tool_use=True
    )

    agent = AssistantAgent(
        name="agent",
        model_client=gpt_4o,
        system_message="你是一个乐于助人的AI智能助手。",
        model_client_stream=True,
        tools=fetch_mcp_server,
        reflect_on_tool_use=True
    )

    agent1 = AssistantAgent(
        name="agent1",
        model_client=deepseek,
        system_message="润色用户提供的内容为微信订阅号风格，并改为markdown格式,字数不要超过1000字",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent2 = AssistantAgent(
        name="agent2",
        model_client=gpt_4o,
        system_message="检查内容是否包含敏感信息，没有则在'S:/AI/AutoGenTest/output'目录,以当前文章标题为文件名，文件名不要超过20个字,且为纯文字，新建markdown文件并写入内容。完成后回复:Pass",
        model_client_stream=True,
        tools=tools_filesystem,
        reflect_on_tool_use=True
    )

    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(4)
    termination = text_termination | max_message_termination
    reflection_team = RoundRobinGroupChat(participants=[agent_search,agent1,agent2], termination_condition=termination, max_turns=None)
    
    stream = reflection_team.run_stream(task="找几句李煜古诗词的巅峰之作")
    await Console(stream)

asyncio.run(main())