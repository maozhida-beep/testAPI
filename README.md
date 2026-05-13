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

Type your message and press Enter. The model streams its reply token by token. Press `Ctrl+C` to exit.

```
=== Terminal Chat Mode (Ctrl+C to quit) ===

You: Hello
AI: Hello! How can I help you today?
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

在终端中输入问题，按回车发送。模型会以流式逐字输出回复。按 `Ctrl+C` 退出。

```
=== 终端对话模式 (Ctrl+C 退出) ===

You: 你好
AI: 你好！有什么可以帮你的？
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
