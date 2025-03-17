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

deepseek=OpenAIChatCompletionClient(
            model="deepseek-chat",
            # api_key="sk-88153123bd974b9c9e8dc02eeaf5ffc4",
            # base_url="https://api.wlai.vip/v1"
        )
        
agent1 = AssistantAgent(
        name="agent1",
        model_client=deepseek,
        system_message="你是古诗词学者，精通各类古诗词，根据提示，给出合适个诗词选段。"
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

termination = text_termination

reflection_team = RoundRobinGroupChat(participants=[agent1, agent2, agent3], termination_condition=termination, max_turns=None)

stream = reflection_team.run_stream(task="说两条让人意难平的诗句")
async def main():
    await Console(stream)

# 运行异步函数
asyncio.run(main())
