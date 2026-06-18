import json
import re
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Lab1-2"))

import todo as todo_mod
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "mistral"
manager = todo_mod.TaskManager()

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the todo list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task title"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "done_task",
            "description": "Mark a task as completed by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_tasks",
            "description": "Search tasks by keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Search keyword"},
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "stats",
            "description": "Get task statistics.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_NAMES = {t["function"]["name"] for t in tools}


def execute_tool(name: str, args: dict) -> str:
    if name == "add_task":
        _, msg = manager.add(args["title"])
        return msg
    if name == "done_task":
        _, msg = manager.done(str(args["task_id"]))
        return msg
    if name == "delete_task":
        _, msg = manager.delete(str(args["task_id"]))
        return msg
    if name == "list_tasks":
        _, msg = manager.list()
        return msg
    if name == "find_tasks":
        _, msg = manager.find(args["keyword"])
        return msg
    if name == "stats":
        _, msg = manager.stats()
        return msg
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
    print("Task Scheduler AI Agent. Type your request in natural language.")
    print("Examples: 'Add a task for paying taxes' or 'Show me all tasks'")
    print("Type 'exit' to quit.\n")

    messages = [
        {"role": "system", "content": "You are a task manager. To manage tasks, output exactly:\nadd_task({\"title\": \"...\"})\ndone_task({\"task_id\": N})\ndelete_task({\"task_id\": N})\nlist_tasks({})\nfind_tasks({\"keyword\": \"...\"})\nstats({})\n\nThen wait for the result and confirm to the user."},
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
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=tools,
            )
            msg = response.choices[0].message

        print(f"AI: {msg.content}\n")


if __name__ == "__main__":
    main()
