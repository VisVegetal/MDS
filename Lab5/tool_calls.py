import json
import re
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Lab1-2"))

import weather as weather_mod
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "mistral"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate an arithmetic expression and return the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to evaluate, e.g. '2 + 3 * 4'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'Bucharest' or 'New York'",
                    }
                },
                "required": ["city"],
            },
        },
    },
]

TOOL_NAMES = {t["function"]["name"] for t in tools}


def execute_tool(name: str, args: dict) -> str:
    if name == "calculate":
        try:
            return str(eval(args["expression"]))
        except Exception as e:
            return f"Error: {e}"
    if name == "get_weather":
        coords = weather_mod.get_coordinates(args["city"])
        if coords is None:
            return f"City '{args['city']}' not found."
        lat, lon = coords
        data = weather_mod.get_weather(lat, lon)
        current = data.get("current", {})
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wcode = current.get("weather_code")
        wind = current.get("wind_speed_10m")
        condition = weather_mod.weather_codes.get(wcode, f"Unknown ({wcode})")
        return (
            f"Weather in {args['city']}: {condition}, "
            f"{temp}°C, humidity {humidity}%, wind {wind} km/h"
        )
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


def call_llm(messages, use_tools):
    kwargs = {"model": MODEL, "messages": messages}
    if use_tools:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs).choices[0].message


def chat_loop(use_tools: bool):
    print(f"Agent with tools={'yes' if use_tools else 'no'}. Type 'exit' to quit.\n")
    messages = [
        {"role": "system", "content": "You are a helpful assistant. When you need to calculate something or check weather, output exactly:\n\ncalculate({\"expression\": \"...\"})\n\nget_weather({\"city\": \"...\"})\n\nThen wait for the result and answer the user."},
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
        msg = call_llm(messages, use_tools)

        tool_calls_list = []
        if use_tools and msg.tool_calls:
            tool_calls_list = [
                (tc.function.name, json.loads(tc.function.arguments))
                for tc in msg.tool_calls
            ]
        elif use_tools and msg.content:
            tool_calls_list = parse_tool_calls(msg.content)

        if tool_calls_list:
            if msg.content:
                messages.append({"role": "assistant", "content": msg.content})
            for name, args in tool_calls_list:
                result = execute_tool(name, args)
                messages.append({"role": "tool", "tool_call_id": "call_1", "content": result})
            msg = call_llm(messages, use_tools)

        print(f"AI: {msg.content}\n")


if __name__ == "__main__":
    use_tools = "--plain" not in sys.argv
    chat_loop(use_tools)
