from langchain.tools import Tool

def echo(input_text: str):
    return f"You said: {input_text}"

def get_tool():
    return Tool(
        name="EchoTool",
        func=echo,
        description=(
            "当你想要把用户的话原样重复回去，用于测试或回显，"
            "例如“帮我重复一句话”之类"
        )
    )
