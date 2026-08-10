#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
DEFAULT_STATE = WORKSPACE / "memory" / "interrupted-tasks.json"


def load(path: Path) -> list:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("state file must contain a JSON array")
    return data


def save(path: Path, data: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def checkpoint(args) -> None:
    data = load(args.state_file)
    existing = next((item for item in data if item.get("taskId") == args.task_id), None)
    entry = existing or {
        "taskId": args.task_id,
        "retryCount": 0,
        "maxRetries": args.max_retries,
        "data": {},
    }
    entry.update({
        "task": args.task,
        "state": "in-progress",
        "interruptible": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    entry["data"]["completedSteps"] = args.completed
    entry["data"]["nextAction"] = args.next_action
    if existing is None:
        data.append(entry)
    save(args.state_file, data)
    print(f"checkpointed: {args.task_id}")


def finish(args, state: str) -> None:
    data = load(args.state_file)
    before = len(data)
    if state == "done":
        data = [item for item in data if item.get("taskId") != args.task_id]
    else:
        for item in data:
            if item.get("taskId") == args.task_id:
                item["state"] = state
                item["timestamp"] = datetime.now(timezone.utc).isoformat()
    if len(data) == before and state == "done" and not any(item.get("taskId") == args.task_id for item in data):
        pass
    save(args.state_file, data)
    print(f"{state}: {args.task_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE)
    sub = parser.add_subparsers(dest="command", required=True)

    cp = sub.add_parser("checkpoint")
    cp.add_argument("--task-id", required=True)
    cp.add_argument("--task", required=True)
    cp.add_argument("--next-action", required=True)
    cp.add_argument("--completed", action="append", default=[])
    cp.add_argument("--max-retries", type=int, default=3)
    cp.set_defaults(func=checkpoint)

    for command in ("complete", "abandon", "fail"):
        item = sub.add_parser(command)
        item.add_argument("--task-id", required=True)
        state = {"complete": "done", "abandon": "abandoned", "fail": "failed"}[command]
        item.set_defaults(func=lambda args, value=state: finish(args, value))

    show = sub.add_parser("show")
    show.set_defaults(func=lambda args: print(json.dumps(load(args.state_file), ensure_ascii=False, indent=2)))

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
