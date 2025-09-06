from langchain.tools import Tool
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 可选表格解析库
try:
    import camelot
except ImportError:
    camelot = None


def parse_pdf(path: str, max_chunks: int = None) -> str:
    """
    使用 pypdf 解析本地 PDF 文件，按段落切分并提取文本，同时提取所有表格并转换为 Markdown。
    支持自定义最大段数，当 max_chunks 为 None 时，返回所有切分段落。

    参数:
    - path: PDF 文件路径
    - max_chunks: 要返回的文本段数，None 时返回全部

    返回:
    - 文本摘要和表格内容的拼接结果
    """
    result_parts = []
    # 1. 提取表格（优先）
    if camelot:
        try:
            tables = camelot.read_pdf(path, pages='all', flavor='stream')
            if tables and tables.n > 0:
                table_texts = []
                for i, table in enumerate(tables, start=1):
                    df = table.df
                    try:
                        md = df.to_markdown(index=False)
                    except Exception:
                        md = df.to_string(index=False)
                    table_texts.append(f"**表格 {i}**：\n{md}")
                result_parts.append("**提取到以下表格内容：**\n" + "\n\n".join(table_texts))
            else:
                result_parts.append("未检测到表格。")
        except Exception as e:
            result_parts.append(f"表格解析失败: {e}")
    else:
        result_parts.append("未安装 camelot，无法提取表格。如需表格解析，请安装 camelot-py[cv]。")

    # 2. 提取文本内容
    try:
        reader = pypdf.PdfReader(path)
        full_text = []
        for page in reader.pages:
            text = page.extract_text() or ""
            full_text.append(text)
        raw = "\n".join(full_text)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        from langchain.docstore.document import Document
        docs = [Document(page_content=raw)]
        chunks = splitter.split_documents(docs)

        if max_chunks is None:
            selected = chunks
        else:
            N = max(0, min(len(chunks), max_chunks))
            selected = chunks[:N]

        snippets = [chunk.page_content.strip() for chunk in selected]
        text_joined = "\n---\n".join(snippets)
        result_parts.append(f"**文本摘要（共 {len(snippets)} 段）**：\n{text_joined}")
    except Exception as e:
        result_parts.append(f"文本解析失败: {e}")

    return "\n\n".join(result_parts)


def get_tool():
    return Tool(
        name="PdfParser",
        func=parse_pdf,
        description=(
            "读取PDF，可选 max_chunks 参数，None 时返回全部文本，对文本做出总结"
            "并提取文档中的所有表格（如果可以的话），返回文本摘要与表格 Markdown，适用于技术资料、协议说明、报表等。"
        )
    )
