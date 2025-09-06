import json
import os
from langchain.chat_models import ChatOpenAI

def get_chat_model(
    api_key: str = " ", # key
    model: str = "gpt-4-0613",
    temperature: float = 0.7
):
    # 如果调用方没传 api_key，就从环境变量里读
    key = api_key or os.getenv("OPENAI_API_KEY")
    if api_key is None:
        with open("configs/config.json", encoding="utf-8") as f:
            api_key=json.load(f)["openai_api_key"]
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=key
    )
