# SPEC: TODO List CLI Application

## 1. Overview

A command-line TODO list application with an interactive REPL (Read-Eval-Print Loop). The user interacts with the application by typing commands at a prompt. All data is persisted to a JSON file on disk.

## 2. Storage

- Tasks are stored in a JSON file named `tasks.json` located in the same directory as the application.
- The file is created automatically on first run if it does not exist.
- Each write operation (add, delete, update) saves the full task list back to the file immediately.

## 3. Task Model

Each task has the following fields:

| Field       | Type    | Description                                                      |
|-------------|---------|------------------------------------------------------------------|
| `id`        | int     | Unique, auto-incrementing identifier                             |
| `title`     | string  | Short description of the task (1–200 characters)                 |
| `done`      | bool    | Whether the task is completed (default: `false`)                 |
| `created_at`| string  | ISO 8601 timestamp when the task was created                     |
| `done_at`   | string? | ISO 8601 timestamp when the task was marked done, or `null`      |

## 4. REPL Commands

The application displays a prompt (by default `> `) and accepts the following commands. Commands are **case-sensitive**.

### 4.1 `add <title>`

Creates a new task with the given title. Whitespace in the title is preserved. If the title exceeds 200 characters, the command is rejected with an error message.

- **Output on success:** `Created task <id>: <title>`
- **Output on error:** `Error: Title must be at most 200 characters.`
- **Edge cases:**
  - Empty title → `Error: Title cannot be empty.`
  - Title with leading/trailing whitespace → the whitespace is stripped.

### 4.2 `done <id>`

Marks the task with the given ID as completed. Sets `done = true` and `done_at` to the current timestamp.

- **Output on success:** `Task <id> marked as done.`
- **Output on error:** `Error: Task <id> not found.`
- **Edge cases:**
  - Marking an already-done task → `Task <id> is already done.` (no change, not an error).
  - Non-numeric id → `Error: Invalid id. Please provide a numeric id.`

### 4.3 `delete <id>`

Permanently removes the task with the given ID from the list.

- **Output on success:** `Deleted task <id>.`
- **Output on error:** `Error: Task <id> not found.`
- **Edge cases:**
  - Non-numeric id → `Error: Invalid id. Please provide a numeric id.`

### 4.4 `list [start_id] [end_id]`

Lists all tasks in the specified ID range (inclusive). If no arguments are given, lists all tasks. If only `start_id` is given, lists from that ID onward.

Tasks are displayed one per line in the format:
```
<id>. [<x| >] <title> (created: <created_at>[, done: <done_at>])
```
where `x` means done and space means not done.

- **Output when no tasks exist:** `No tasks found.`
- **Output on error for invalid ids:** `Error: Invalid id. Please provide numeric ids.`
- **Edge cases:**
  - If `start_id` > `end_id`, swap them so the range is always valid.
  - If no tasks match the range, show `No tasks found.`
  - Completed tasks show their `done_at` timestamp; pending tasks omit it.

### 4.5 `find <keyword>`

Searches for tasks whose title contains the given keyword (case-insensitive substring match).

- **Output:** Same format as `list`, but only matching tasks.
- **Output when no matches:** `No tasks found.`
- **Edge cases:** Empty keyword → `Error: Keyword cannot be empty.`

### 4.6 `stats`

Displays statistics about the task list:
```
Total tasks: <N>
Completed: <M>
Pending: <P>
```

### 4.7 `help`

Displays a brief help message listing all available commands with their syntax.

### 4.8 `exit` / `quit`

Exits the REPL.

## 5. Error Handling

- Unknown commands → `Unknown command: <cmd>. Type 'help' for available commands.`
- Invalid argument types (non-numeric where numeric expected) → `Error: Invalid id. Please provide a numeric id.`
- Missing required arguments → `Error: Missing argument. Usage: <command> <args>`
- The application must never crash due to user input. All exceptions are caught and displayed as `Error: <message>`.

## 6. Implementation Requirements

- Language: **Python 3.10+**
- No external dependencies beyond the Python standard library.
- The main entry point is `todo.py`.
- The file `tasks.json` must be human-readable (indented JSON).
- Code must be clean, with functions under 30 lines where possible.
