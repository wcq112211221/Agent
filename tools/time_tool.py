# tools/time_tool.py
from langchain.tools import Tool
from datetime import datetime

def get_time(_):
    return datetime.now().strftime("现在是 %Y-%m-%d %H:%M:%S")

def get_tool():
    return Tool(
        name="TimeTool",
        func=get_time,
        description=(
            "当用户想要知道当前本地时间时，就调用这个工具，"
            "比如“现在几点了”“当前时间”之类的问句"
        )
    )
