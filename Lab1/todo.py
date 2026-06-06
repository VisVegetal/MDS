import json
import os
from datetime import datetime, timezone


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._load()

    def _load(self):
        if not os.path.exists(DATA_FILE):
            self.tasks = []
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.tasks = []

    def _save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def _next_id(self):
        if not self.tasks:
            return 1
        return max(t["id"] for t in self.tasks) + 1

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def add(self, title):
        title = title.strip()
        if not title:
            return False, "Error: Title cannot be empty."
        if len(title) > 200:
            return False, "Error: Title must be at most 200 characters."
        task = {
            "id": self._next_id(),
            "title": title,
            "done": False,
            "created_at": self._now(),
            "done_at": None,
        }
        self.tasks.append(task)
        self._save()
        return True, f"Created task {task['id']}: {title}"

    def done(self, raw_id):
        try:
            tid = int(raw_id)
        except ValueError:
            return False, "Error: Invalid id. Please provide a numeric id."
        for t in self.tasks:
            if t["id"] == tid:
                if t["done"]:
                    return False, f"Task {tid} is already done."
                t["done"] = True
                t["done_at"] = self._now()
                self._save()
                return True, f"Task {tid} marked as done."
        return False, f"Error: Task {tid} not found."

    def delete(self, raw_id):
        try:
            tid = int(raw_id)
        except ValueError:
            return False, "Error: Invalid id. Please provide a numeric id."
        for i, t in enumerate(self.tasks):
            if t["id"] == tid:
                del self.tasks[i]
                self._save()
                return True, f"Deleted task {tid}."
        return False, f"Error: Task {tid} not found."

    def list(self, raw_start=None, raw_end=None):
        tasks = self.tasks
        if raw_start is not None:
            try:
                start = int(raw_start)
            except ValueError:
                return False, "Error: Invalid id. Please provide numeric ids."
            if raw_end is not None:
                try:
                    end = int(raw_end)
                except ValueError:
                    return False, "Error: Invalid id. Please provide numeric ids."
            else:
                end = None
            if end is not None and start > end:
                start, end = end, start
            if end is not None:
                tasks = [t for t in tasks if start <= t["id"] <= end]
            else:
                tasks = [t for t in tasks if t["id"] >= start]
        if not tasks:
            return True, "No tasks found."
        lines = []
        for t in tasks:
            marker = "x" if t["done"] else " "
            done_part = ""
            if t["done"] and t["done_at"]:
                done_part = f", done: {t['done_at']}"
            lines.append(f"{t['id']}. [{marker}] {t['title']} (created: {t['created_at']}{done_part})")
        return True, "\n".join(lines)

    def find(self, keyword):
        if not keyword:
            return False, "Error: Keyword cannot be empty."
        matches = [t for t in self.tasks if keyword.lower() in t["title"].lower()]
        if not matches:
            return True, "No tasks found."
        lines = []
        for t in matches:
            marker = "x" if t["done"] else " "
            done_part = ""
            if t["done"] and t["done_at"]:
                done_part = f", done: {t['done_at']}"
            lines.append(f"{t['id']}. [{marker}] {t['title']} (created: {t['created_at']}{done_part})")
        return True, "\n".join(lines)

    def stats(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["done"])
        pending = total - completed
        return True, f"Total tasks: {total}\nCompleted: {completed}\nPending: {pending}"


def print_help():
    lines = [
        "Available commands:",
        "  add <title>          Create a new task",
        "  done <id>            Mark a task as completed",
        "  delete <id>          Delete a task",
        "  list [start] [end]   List tasks (optional id range)",
        "  find <keyword>       Search tasks by keyword",
        "  stats                Show task statistics",
        "  help                 Show this help message",
        "  exit / quit          Exit the application",
    ]
    print("\n".join(lines))


def main():
    manager = TaskManager()
    print("TODO List CLI. Type 'help' for commands.")
    while True:
        try:
            cmd_line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not cmd_line:
            continue
        parts = cmd_line.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ("exit", "quit"):
            break
        elif cmd == "help":
            print_help()
            continue
        elif cmd == "add":
            _, _, rest = cmd_line.partition(" ")
            success, msg = manager.add(rest)
            print(msg)
        elif cmd == "done":
            if not args:
                print("Error: Missing argument. Usage: done <id>")
                continue
            success, msg = manager.done(args)
            print(msg)
        elif cmd == "delete":
            if not args:
                print("Error: Missing argument. Usage: delete <id>")
                continue
            success, msg = manager.delete(args)
            print(msg)
        elif cmd == "list":
            if args:
                range_parts = args.split()
                if len(range_parts) == 1:
                    success, msg = manager.list(raw_start=range_parts[0])
                else:
                    success, msg = manager.list(raw_start=range_parts[0], raw_end=range_parts[1])
            else:
                success, msg = manager.list()
            print(msg)
        elif cmd == "find":
            if not args:
                print("Error: Missing argument. Usage: find <keyword>")
                continue
            success, msg = manager.find(args)
            print(msg)
        elif cmd == "stats":
            success, msg = manager.stats()
            print(msg)
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
