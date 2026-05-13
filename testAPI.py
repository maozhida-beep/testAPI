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

print("=== 终端对话模式 (Ctrl+C 退出) ===\n")

try:
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        stream = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            max_tokens=102400,
            temperature=0.7,
            stream=True,
        )

        print("AI: ", end="", flush=True)
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print("\n")

        messages.append({"role": "assistant", "content": full_response})

except KeyboardInterrupt:
    print("\n\n已退出对话。")
