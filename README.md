# DeepSeek Terminal Chat / DeepSeek 终端对话

[English](#english) | [中文](#中文)

---

## English

An interactive terminal chatbot powered by DeepSeek API, with streaming output and multi-turn conversation support.

**No code. No browser.** Just talk to DeepSeek right from your terminal.

### Quick Start

**1. Install dependencies**

```bash
pip install openai
```

**2. Set your API key**

```bash
export DEEPSEEK_API_KEY='your-api-key'
```

Or use a `.env` file (see `.env.example`):

```bash
cp .env.example .env
# edit .env with your key
source .env
```

**3. Run**

```bash
python testAPI.py
```

**4. Chat**

Type your message and press Enter to send. The model streams its reply token by token.

```
You: Hello
AI: Hello! How can I help you today?
```

### Commands

| Command   | Description                      |
|-----------|----------------------------------|
| `/lines`  | Enter multi-line input mode      |
| `/single` | Return to single-line mode       |
| `/clear`  | Clear conversation history       |
| `Ctrl+C`  | Exit                             |

Use `/lines` to enter multi-line mode for pasting code or long text. In multi-line mode, press Enter twice in a row to send. Use `/single` to return to single-line mode.

```
You: /lines
[Multi-line mode on]

[Multi-line mode] ... Explain this code:
... def fib(n):
...     return n if n <= 1 else fib(n-1) + fib(n-2)
... 
... 
You: /single
[Single-line mode]

You: Thanks!
AI: You're welcome!
```

### Configuration

Tweak these parameters in `testAPI.py`:

| Parameter    | Description           | Default            |
|-------------|-----------------------|--------------------|
| `model`     | Model name            | `deepseek-v4-pro`  |
| `max_tokens` | Max response length  | 102400             |
| `temperature` | Randomness (0-2)    | 0.7                |

### License

MIT

---

## 中文

基于 DeepSeek API 的交互式终端对话工具，支持流式输出和多轮对话。

**无需写代码、无需打开网页**，在终端里就能与 DeepSeek 自由对话。

### 快速开始

**1. 安装依赖**

```bash
pip install openai
```

**2. 设置 API Key**

```bash
export DEEPSEEK_API_KEY='your-api-key'
```

或创建 `.env` 文件（参考 `.env.example`）：

```bash
cp .env.example .env
# 编辑 .env 填入你的 key
source .env
```

**3. 运行**

```bash
python testAPI.py
```

**4. 使用**

输入内容后按回车发送，模型以流式逐字输出回复。

```
You: 你好
AI: 你好！有什么可以帮你的？
```

### 命令

| 命令 | 说明 |
|------|------|
| `/lines` | 进入多行输入模式 |
| `/single` | 回到单行输入模式 |
| `/clear` | 清空对话历史 |
| `Ctrl+C` | 退出程序 |

使用 `/lines` 进入多行模式，可粘贴代码块或长文本。多行模式下连按两次回车发送，使用 `/single` 切回单行模式。

```
You: /lines
[多行输入已开启]

[多行模式] ... 解释一下这段代码:
... def fib(n):
...     return n if n <= 1 else fib(n-1) + fib(n-2)
... 
... 
You: /single
[单行输入模式]

You: 谢谢！
AI: 不客气！
```

### 配置

可在 `testAPI.py` 中调整以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `model` | 模型名称 | `deepseek-v4-pro` |
| `max_tokens` | 最大回复长度 | 102400 |
| `temperature` | 生成随机性 (0-2) | 0.7 |

### 许可

MIT
