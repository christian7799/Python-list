#!/usr/bin/env python3
"""
todo.py — Mini app de linha de comando para gerenciar uma lista de tarefas.

Como usar:
    python todo.py add "Comprar pão"
    python todo.py list
    python todo.py done 2
    python todo.py remove 3
    python todo.py clear

O arquivo de dados é criado automaticamente: todos.json

"""
import sys
import json
from pathlib import Path

DATA_FILE = Path("todos.json")


def load_todos():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")


def add_task(text):
    todos = load_todos()
    todos.append({"task": text, "done": False})
    save_todos(todos)
    print(f'Adicionada: "{text}" (id {len(todos)})')


def list_tasks():
    todos = load_todos()
    if not todos:
        print("Nenhuma tarefa encontrada. Use: python todo.py add \"Minha tarefa\"")
        return
    for i, item in enumerate(todos, start=1):
        status = "✓" if item.get("done") else " "
        print(f"{i:2}. [{status}] {item.get('task')}")


def mark_done(idx):
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        print("ID inválido.")
        return
    todos[idx - 1]["done"] = True
    save_todos(todos)
    print(f"Tarefa {idx} marcada como concluída.")


def remove_task(idx):
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        print("ID inválido.")
        return
    removed = todos.pop(idx - 1)
    save_todos(todos)
    print(f'Removida: "{removed.get("task")}"')


def clear_tasks():
    save_todos([])
    print("Todas as tarefas removidas.")


def print_help():
    print(__doc__)


def main(argv):
    if len(argv) < 2:
        print_help()
        return

    cmd = argv[1].lower()

    if cmd == "add" and len(argv) >= 3:
        add_task(" ".join(argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd in ("done", "complete") and len(argv) == 3 and argv[2].isdigit():
        mark_done(int(argv[2]))
    elif cmd == "remove" and len(argv) == 3 and argv[2].isdigit():
        remove_task(int(argv[2]))
    elif cmd == "clear":
        clear_tasks()
    else:
        print("Comando inválido ou falta de argumentos.")
        print_help()


if __name__ == "__main__":
    main(sys.argv)
