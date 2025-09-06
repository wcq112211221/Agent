from mcp.gpt_based import get_chat_model
from tools import load_all_tools
from langchain.agents import initialize_agent, AgentType

def get_agent():
    llm = get_chat_model()         # 不需要在此处显式传 key
    tools = load_all_tools()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,  # 打开后你可以在输出里看到模型的 chain-of-thought
        max_iterations=3,  # 最多三次工具调用循环
        early_stopping_method="generate",
        handle_parsing_errors=True,
    )
    return agent