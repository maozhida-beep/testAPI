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

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]


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
            print("[多行输入已开启]\n")
            continue

        if clean_cmd(user_input) == "/single":
            multiline = False
            print("[单行输入模式]\n")
            continue

        if clean_cmd(user_input) == "/clear":
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
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
    print("\n\n已退出对话。")
