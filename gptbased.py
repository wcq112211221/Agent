import streamlit as st
from mcp.dispatcher import get_agent
from tools import load_all_tools
import tempfile
import os

# 初始化工具和 Agent
tools = load_all_tools()
agent = get_agent()

# Streamlit 设置
st.title("🤖 GPT-4.1 + 工具调用聊天助手")
st.divider()

# PDF 上传
uploaded_file = st.file_uploader("上传 PDF 文档", type="pdf")
if uploaded_file is not None:
    # 保存到临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name
    st.success(f"已上传：{os.path.basename(pdf_path)}")
else:
    pdf_path = None

# 聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入框
if prompt := st.chat_input("请输入问题或命令…"):
    # 记录用户输入
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 如果有上传 PDF，优先调用 PdfParser
    if pdf_path and "pdf_summary" not in st.session_state:
        try:
            pdf_summary=agent.run(f"PdfParser\n{pdf_path}")
            st.session_state["pdf_summary"]=pdf_summary
            st.chat_message("assistant").markdown(f"**PDF 摘要：**\n{pdf_summary}")
            st.session_state.messages.append({"role": "assistant", "content": pdf_summary})
        except Exception as e:
            st.error(f"PDF 解析失败: {e}")

    # 普通对话 / 工具调用
    try:
        reply = agent.run(prompt)
    except Exception as e:
        reply = f"❌ 工具调用失败: {e}"

    # 展示并存储助手回复
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
