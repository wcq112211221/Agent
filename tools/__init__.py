import importlib
import os

def load_all_tools():
    tool_list = []
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith("_tool.py"):
            module_name = f"tools.{filename[:-3]}"
            module = importlib.import_module(module_name)
            tool = module.get_tool()
            tool_list.append(tool)
    return tool_list
