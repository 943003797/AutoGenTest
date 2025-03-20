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
    # 获取当前项目路径
    project_path = os.path.dirname(os.path.abspath(__file__))+"\\output"
    tools_filesystem = await mcp_server_tools(StdioServerParams(command="npx.cmd", args=["-y", "@modelcontextprotocol/server-filesystem", project_path]))

    # fetch_mcp_server = await mcp_server_tools(StdioServerParams(command="python", args=["mcp/mcp_server_fetch.py"]))

    # tools_firecrawl = await mcp_server_tools(StdioServerParams(
    #   command= "cmd",
    #   args= [
    #     "/c",
    #     "npx",
    #     "-y",
    #     "@smithery/cli@latest",
    #     "run",
    #     "@mendableai/mcp-server-firecrawl",
    #     "--config",
    #     "{\"fireCrawlApiKey\":\"fc-e7b183b16de64e6a85b009920c68cb10\"}"
    #   ]
    # ))

    # tools_duckduckgo = await mcp_server_tools(StdioServerParams(
    #     command= "cmd",
    #   args= [
    #     "/c",
    #     "npx",
    #     "-y",
    #     "@smithery/cli@latest",
    #     "run",
    #     "@nickclyde/duckduckgo-mcp-server",
    #     "--config",
    #     "{}"
    #   ]
    # ))

    # tools_tavily = await mcp_server_tools(StdioServerParams(
    #   command= "cmd",
    #   args= [
    #     "/c",
    #     "npx",
    #     "-y",
    #     "@smithery/cli@latest",
    #     "run",
    #     "tavily-search",
    #     "--config",
    #     "{\"tavilyApiKey\":\"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\"}"
    #   ]
    # ))

    agent_search = AssistantAgent(
        name="agent",
        model_client=deepseek,
        system_message="你是短视频古诗词文案大师，用户会给出本期标题，你要给出适合的诗句,只列举诗句和选自那首诗，不要给出其他内容。",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent = AssistantAgent(
        name="agent",
        model_client=gpt_4o,
        system_message="你是个信息搜索整理助手,会使用网络搜索相关信息，整理给用户",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent1 = AssistantAgent(
        name="agent1",
        model_client=deepseek,
        system_message="润色用户提供的内容为抖音诗词文案风格，一首诗只取精华部分，最后整理为markdown格式,字数不要超过300字",
        model_client_stream=True,
        reflect_on_tool_use=True
    )

    agent2 = AssistantAgent(
        name="agent2",
        model_client=gpt_4o,
        system_message="检查内容是否包含敏感信息，没有则以当前文章标题为文件名，文件名不要超过20个字,且为纯文字，在"+project_path+"新建markdown文件并写入内容。完成后回复:Pass",
        model_client_stream=True,
        tools=tools_filesystem,
        reflect_on_tool_use=True
    )

    text_termination = TextMentionTermination("Pass")
    max_message_termination = MaxMessageTermination(4)
    termination = text_termination | max_message_termination
    reflection_team = RoundRobinGroupChat(participants=[agent,agent2], termination_condition=termination, max_turns=None)
    
    stream = reflection_team.run_stream(task="写一个介绍Autogen的PPT，包含介绍，安装，使用，扩展等内容")
    await Console(stream)

asyncio.run(main())