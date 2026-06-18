import json
import re
import subprocess
import sys
import os

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "mistral"

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file"},
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file (overwrites existing).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file"},
                    "content": {"type": "string", "description": "File content"},
                },
                "required": ["file_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"},
                },
                "required": ["command"],
            },
        },
    },
]

TOOL_NAMES = {t["function"]["name"] for t in tools}


def confirm(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False


def execute_tool(name: str, args: dict) -> str:
    if name == "read_file":
        path = args["file_path"]
        if not confirm(f"Read file: {path}"):
            return "Operation cancelled."
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    if name == "write_file":
        path = args["file_path"]
        preview = args["content"][:300]
        if len(args["content"]) > 300:
            preview += " [... truncated]"
        if not confirm(f"Write to file: {path}\n---\n{preview}\n---"):
            return "Operation cancelled."
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(args["content"])
            return f"Wrote {len(args['content'])} bytes to {path}"
        except Exception as e:
            return f"Error: {e}"

    if name == "run_command":
        cmd = args["command"]
        if not confirm(f"Run command: {cmd}"):
            return "Operation cancelled."
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout
            if result.stderr:
                output += "\nSTDERR:\n" + result.stderr
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out."
        except Exception as e:
            return f"Error: {e}"

    return f"Unknown tool: {name}"


def parse_tool_calls(text: str):
    pattern = r"(\w+)\s*\(\s*(\{.*?\})\s*\)"
    matches = re.findall(pattern, text, re.DOTALL)
    result = []
    for name, args_str in matches:
        if name in TOOL_NAMES:
            try:
                args = json.loads(args_str)
                result.append((name, args))
            except json.JSONDecodeError:
                pass
    return result


def main():
    print("Coding Agent. I can read/write files and run commands.")
    print("Every tool requires your approval. Type 'exit' to quit.\n")

    messages = [
        {"role": "system", "content": "You are a coding assistant. To perform actions, output exactly:\nread_file({\"file_path\": \"...\"})\nwrite_file({\"file_path\": \"...\", \"content\": \"...\"})\nrun_command({\"command\": \"...\"})\n\nThen wait for the result and continue helping the user."},
    ]

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user})
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools,
        )
        msg = response.choices[0].message

        tool_calls_list = []
        if msg.tool_calls:
            tool_calls_list = [
                (tc.function.name, json.loads(tc.function.arguments))
                for tc in msg.tool_calls
            ]
        elif msg.content:
            tool_calls_list = parse_tool_calls(msg.content)

        if tool_calls_list:
            if msg.content:
                messages.append({"role": "assistant", "content": msg.content})
            for name, args in tool_calls_list:
                result = execute_tool(name, args)
                messages.append({"role": "tool", "tool_call_id": "call_1", "content": result})
                print(f"  -> {name}: {result}")
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=tools,
            )
            msg = response.choices[0].message

        print(f"AI: {msg.content}\n")


if __name__ == "__main__":
    main()
