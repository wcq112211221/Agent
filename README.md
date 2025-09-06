# LightRAG

**状态**: 🚧 WIP（进行中 — 用于学习与持续更新）

一个基于 LangChain 的轻量 Agent 框架演示，包含若干工具（PDF 解析、HTTP 抓取、时间工具、回显工具）、Streamlit 前端示例以及 Agent 初始化逻辑。该仓库为学习与实验用途，当前部分模块仍在开发中（见 "未完成 / TODO"）。

---

## 快速开始（拷贝即用）

1. 克隆或解压项目后，进入项目根目录：

```bash
cd agentragsys
```

2. 创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.\.venv\Scripts\activate   # Windows (PowerShell)
```

3. 安装依赖（`requirements.txt` 当前为空，请见下方建议依赖）：

```bash
pip install -r requirements.txt
# 或者临时安装推荐依赖：
pip install langchain openai streamlit pypdf camelot-py-bs4 requests beautifulsoup4
```

4. 配置 OpenAI Key（优先使用环境变量）

```bash
export OPENAI_API_KEY="your_openai_api_key"
# 或者编辑 configs/config.json（注意不要把真实 key 提交到 Git）
```

5. 启动 Streamlit 前端（示例）：

```bash
streamlit run agentragsys/gptbased.py
```

> 如果遇到 `ModuleNotFoundError`，请确认当前工作目录包含 `agentragsys` 包，或将项目根加入 `PYTHONPATH`。

---

## 项目结构（概要）

```
agentragsys/
  ├─ gptbased.py          # Streamlit 演示：初始化工具 + agent 并提供上传 PDF 等功能
  ├─ main.py              # 目前为空（可作为 CLI / 程序入口）
  ├─ configs/config.json  # 示例配置（当前为占位 key）
  ├─ tools/               # 自定义工具集合（以 *_tool.py 自动加载）
  │   ├─ pdf_tool.py      # PDF 解析 -> 文本 + 表格 -> Markdown
  │   ├─ http_tool.py     # HTTP 抓取 + 简单解析（requests + BeautifulSoup）
  │   ├─ time_tool.py     # 返回当前时间
  │   └─ echo_tool.py     # 测试回显工具
  ├─ mcp/                 # Agent 初始化与 schema
  │   ├─ gpt_based.py     # LangChain Chat 模型封装（get_chat_model）
  │   ├─ dispatcher.py    # initialize_agent 调用（加载工具 + 配置 AgentType）
  │   └─ schema.py        # pydantic ToolCall 等（简单 schema）
  ├─ rag/                 # （空）RAG 相关代码占位
  ├─ memory/              # （空）长期/短期记忆模块占位
  └─ models/              # （空）模型/向量存储占位
```

**注意（当前仓库观察到的状态）**

* `agentragsys/README.md` 和 `requirements.txt` 目前为空。请在发布前补全依赖与说明。
* `agentragsys/main.py` 是空文件，建议补充为 CLI/服务启动入口或删除保持清晰。
* `configs/config.json` 有 `"openai_api_key": "key"` 占位，请不要把真实 key 提交到代码库。
* 仓库包含 `.venv/`（虚拟环境），建议不要把虚拟环境提交到 git（在 `.gitignore` 中添加 `.venv/`），而是提供 `requirements.txt`。

---

## 技术要点（针对代码的重点说明）

1. **LangChain Agent 架构**

   * 使用 `initialize_agent(..., agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)`，适合工具链驱动的问答流程（模型决定何时调用工具）。
   * `max_iterations=3`、`early_stopping_method="generate"` 已设置，注意调优以防工具滥用或超时。

2. **工具（Tool）设计模式**

   * `tools/__init__.py` 通过扫描以 `_tool.py` 结尾的模块自动加载工具，工具模块应暴露 `get_tool()` 返回 `langchain.tools.Tool` 对象。
   * 每个工具应做入参校验、异常捕获和可重试逻辑（当前实现中对异常处理较简单，建议完善）。

3. **PDF 解析**

   * 使用 `pypdf` 提取文本，再用 `RecursiveCharacterTextSplitter` 切块；可选使用 `camelot` 提取表格并转成 Markdown。
   * 对于大型 PDF 建议限制 `max_chunks` 或使用分批流式索引（向量化/FAISS）以降低内存与响应延迟。

4. **HTTP 抓取工具**

   * `http_tool.py` 使用 `requests` + `BeautifulSoup` 提取文章标题与前若干段落，适合作为检索前的快速预处理。
   * 生产环境需处理更多异常（重试、超时、robots、反爬机制）与字符编码问题。

5. **模型调用封装**

   * `mcp/gpt_based.get_chat_model()` 封装 `ChatOpenAI`（LangChain），从环境变量或 `configs/config.json` 获取 key。
   * 注意：配置密钥的优先级与安全性（建议优先使用环境变量或 secret 管理器，避免明文存储）。

6. **可扩展性与 RAG（占位）**

   * 已留出 `rag/`、`memory/`、`models/` 目录。实现 RAG 时要考虑：文档分块、Embedding（OpenAI/本地模型）、向量索引（FAISS/Annoy/Chroma）、检索策略（top-k、score threshold）。

7. **工程实践**

   * 移除 `.venv/`、添加 `.gitignore`、补全 `requirements.txt`（并锁版本）、考虑 `pyproject.toml` 或 `setup.cfg`。
   * 添加单元测试、静态检查（flake8/ruff/mypy）和 CI（GitHub Actions）；封装 Dockerfile 以便部署。

---

## 优先级 TODO（建议按顺序完成）

1. **补全 `requirements.txt` 并删掉 `.venv/`**（高优先）
2. **实现或移除 `main.py`**：增加 CLI（`click`）或入口脚本以便生产运行。
3. **完善配置管理**：添加 `configs/config.json.sample`、`.env` 支持，并把密钥从仓库移除。
4. **实现 RAG 基线**：向量化 + FAISS 索引 + 简单检索接口（目录 `rag/`）。
5. **增加 logging、异常与熔断策略**：工具调用必须有超时、重试与日志。
6. **安全与隐私**：避免将密钥与敏感数据提交，审查第三方依赖。
7. **测试 + CI + Docker**：保证可复现的环境与自动化检测。

---

## 建议的 `requirements.txt` （示例，可根据需要锁版本）

```
langchain
openai
streamlit
pypdf
camelot-py[cv]
beautifulsoup4
requests
pydantic
```

> 注：`camelot` 依赖较多（需要系统库），如只需文本解析可先不安装。

---

## 贡献指南（简单）

1. Fork -> 新建分支 -> 提交 -> 发起 PR。
2. 代码风格：尽量使用类型注解、docstring、并通过 linter（如 ruff/flake8）。
3. PR 内容请包含变更说明与复现步骤。

---


---

## 联系

欢迎一起学习交流

