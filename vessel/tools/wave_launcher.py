#!/usr/bin/env python3
"""
Super Z Wave Launcher — Helper for planning parallel agent waves.

Usage:
    python vessel/tools/wave_launcher.py plan "task1, task2, task3, task4"
    python vessel/tools/wave_launcher.py status

This tool helps plan and track wave-based parallel execution.
It does NOT launch agents (that's the LLM runtime's job), but it
provides structure for wave planning.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(os.environ.get("SUPERZ_REPO_ROOT", Path(__file__).resolve().parent.parent.parent))
WAVE_STATE_PATH = Path(os.environ.get("SUPERZ_WAVE_STATE_PATH", REPO_ROOT / "agent-personallog" / "wave-state.json"))


def parse_tasks(task_string):
    """Parse comma-separated task descriptions into task objects."""
    tasks = []
    for i, desc in enumerate(task_string.split(",")):
        desc = desc.strip()
        if desc:
            tasks.append({
                "id": i + 1,
                "description": desc,
                "wave": 1,  # Default: all in wave 1 (parallel)
                "status": "pending",
                "dependencies": [],
                "result": None
            })
    return tasks


def assign_waves(tasks):
    """Assign wave numbers based on dependencies (all independent = wave 1)."""
    # Simple heuristic: if no dependencies specified, all go in wave 1
    # More sophisticated dependency resolution can be added
    for task in tasks:
        if task["dependencies"]:
            max_dep_wave = max(
                next((t["wave"] for t in tasks if t["id"] == dep), 0)
                for dep in task["dependencies"]
            )
            task["wave"] = max_dep_wave + 1
    return tasks


def plan(args):
    """Plan waves for a set of tasks."""
    if len(args) < 2:
        print("Usage: wave_launcher.py plan \"task1, task2, task3\"")
        print()
        print("Tasks are comma-separated. All tasks go in Wave 1 by default.")
        print("To specify dependencies, use: task1::dep_on_1,dep_on_2")
        return 1

    task_string = args[1]
    tasks = parse_tasks(task_string)

    # Check for dependency syntax (task::dep1,dep2)
    for task in tasks:
        if "::" in task["description"]:
            parts = task["description"].split("::")
            task["description"] = parts[0].strip()
            task["dependencies"] = [int(d.strip()) for d in parts[1].split(",")]

    tasks = assign_waves(tasks)

    # Group by wave
    waves = {}
    for task in tasks:
        wave = task["wave"]
        if wave not in waves:
            waves[wave] = []
        waves[wave].append(task)

    print("=== Wave Plan ===")
    print()
    for wave_num in sorted(waves.keys()):
        wave_tasks = waves[wave_num]
        print(f"Wave {wave_num} ({len(wave_tasks)} tasks, parallel):")
        for t in wave_tasks:
            dep_str = f" [depends on: {t['dependencies']}]" if t['dependencies'] else ""
            print(f"  [{t['id']}] {t['description']}{dep_str}")
        print()

    # Save state
    state = {
        "created": datetime.now(timezone.utc).isoformat(),
        "total_tasks": len(tasks),
        "total_waves": len(waves),
        "tasks": tasks,
        "waves": {str(k): len(v) for k, v in waves.items()}
    }
    WAVE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(WAVE_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Wave state saved to {WAVE_STATE_PATH}")
    return 0


def status(args):
    """Show current wave state."""
    if not WAVE_STATE_PATH.exists():
        print("No active wave plan. Run 'wave_launcher.py plan' first.")
        return 1

    with open(WAVE_STATE_PATH, "r") as f:
        state = json.load(f)

    print("=== Wave Status ===")
    print(f"Created: {state['created']}")
    print(f"Total Tasks: {state['total_tasks']}")
    print(f"Total Waves: {state['total_waves']}")
    print()

    for wave_num, count in state["waves"].items():
        wave_tasks = [t for t in state["tasks"] if str(t["wave"]) == wave_num]
        completed = sum(1 for t in wave_tasks if t["status"] == "completed")
        print(f"Wave {wave_num}: {completed}/{count} completed")
        for t in wave_tasks:
            status_icon = "✓" if t["status"] == "completed" else "○"
            print(f"  {status_icon} [{t['id']}] {t['description']} ({t['status']})")
    return 0


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    if not args or args[0] == "help":
        print("Super Z Wave Launcher v1.0.0")
        print()
        print("Commands:")
        print("  plan \"task1, task2, ...\"   Plan waves for tasks")
        print("  status                       Show current wave state")
        print("  help                         Show this help")
        return 0

    if args[0] == "plan":
        return plan(args)
    elif args[0] == "status":
        return status(args)
    else:
        print(f"Unknown command: {args[0]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
