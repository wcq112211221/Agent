# mcp/schema.py
from pydantic import BaseModel
from typing import Literal, Dict, Any

class ToolCall(BaseModel):
    tool: str               # 工具名称，比如 "get_date"
    args: Dict[str, Any]    # 参数字典
