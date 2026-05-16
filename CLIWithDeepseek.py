import os
import sys
from openai import OpenAI

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("错误: 请设置环境变量 DEEPSEEK_API_KEY")
    print("  export DEEPSEEK_API_KEY='your-api-key'")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

MEMORY_DIR = os.path.expanduser("~/.cliwithdeepseek")
MEMORY_FILE = os.path.join(MEMORY_DIR, "memory.md")


def load_memory():
    if os.path.exists(MEMORY_FILE):
        content = open(MEMORY_FILE, encoding="utf-8").read().strip()
        if content:
            print(f"[记忆已加载 / Memory loaded: {MEMORY_FILE}]\n")
        return content
    return ""


def build_system_prompt(memory):
    content = "You are a helpful assistant."
    if memory:
        content += f"\n\nInformation about the user you are talking to:\n{memory}"
    return content


def save_memory(messages, old_memory):
    conv = [m for m in messages if m["role"] != "system"]
    if len(conv) < 2:
        return old_memory

    # Only use recent exchanges to keep the summary call lean
    recent = conv[-30:]

    prompt = (
        "Extract key information about the user from this conversation. "
        "Include: name, role, preferences, ongoing projects, tools they use, "
        "and any other details that would help an AI assistant understand who they are. "
        "Write in second person ('You are...', 'You prefer...'). "
        "Be concise, 2-5 bullet points. Only include what can be confirmed from the conversation.\n\n"
    )

    if old_memory:
        prompt += f"Existing memory about the user:\n{old_memory}\n\n"
        prompt += "Update this with new information from the conversation above. "
        prompt += "Keep existing info that hasn't changed, add new info, remove contradicted info."

    try:
        summary_messages = [
            {"role": "system", "content": "You extract user profile information from conversations. Be concise and factual."},
            *recent,
            {"role": "user", "content": prompt},
        ]
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=summary_messages,
            max_tokens=500,
            temperature=0.3,
            stream=False,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return old_memory


def clean_cmd(text):
    """Strip whitespace and encoding noise for command matching."""
    return text.strip().replace("�", "").strip()


def read_multiline():
    """Read multi-line input. /lines or /clear on their own line exits immediately."""
    lines = []
    blank_count = 0
    print("... ", end="", flush=True)
    while True:
        line = input()
        lines.append(line)

        if len(lines) == 1 and clean_cmd(line) in ("/lines", "/single", "/clear"):
            return clean_cmd(line)

        if line.strip() == "":
            blank_count += 1
            if blank_count >= 2:
                while lines and lines[-1].strip() == "":
                    lines.pop()
                return "\n".join(lines)
        else:
            blank_count = 0


def send_message(stream):
    print("AI: ", end="", flush=True)
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    print("\n")
    return full_response


memory = load_memory()
messages = [
    {"role": "system", "content": build_system_prompt(memory)},
]

print("=== 终端对话 | /lines 多行 | /single 单行 | /clear 清空 | Ctrl+C 退出 ===\n")

multiline = False

try:
    while True:
        if multiline:
            print("[多行模式] ", end="")
        user_input = read_multiline() if multiline else input("You: ")

        stripped = user_input.strip()
        if not stripped:
            continue

        if clean_cmd(user_input) == "/lines":
            multiline = True
            print("[多行输入已开启 / Multi-line on (double-Enter to send)]\n")
            continue

        if clean_cmd(user_input) == "/single":
            multiline = False
            print("[单行输入模式]\n")
            continue

        if clean_cmd(user_input) == "/clear":
            messages = [
                {"role": "system", "content": build_system_prompt(memory)},
            ]
            print("[对话历史已清空]\n")
            continue

        messages.append({"role": "user", "content": user_input})

        stream = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            max_tokens=102400,
            temperature=0.7,
            stream=True,
        )

        full_response = send_message(stream)
        messages.append({"role": "assistant", "content": full_response})

except KeyboardInterrupt:
    print("\n\n正在保存记忆 / Saving memory...")
    new_memory = save_memory(messages, memory)
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write(new_memory + "\n")
    print("已退出对话 / Goodbye.")
