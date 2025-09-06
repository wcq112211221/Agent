import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool

def fetch_and_parse(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # ——示例：提取文章标题和正文
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    paragraphs = soup.find_all("p")
    content = "\n".join(p.get_text(strip=True) for p in paragraphs[:10])  # 只取前10段

    return f"标题：{title}\n正文片段：\n{content}"

def get_tool():
    return Tool(
        name="HttpParse",
        func=fetch_and_parse,
        description=(
            "输入一个网址，爬取该页面的 H1 标题和正文，（无需额外引号）。并做总结，要求如果是学术内容深入理解"
            "适用于典型的新闻页面或文章页面。"
        )
    )
