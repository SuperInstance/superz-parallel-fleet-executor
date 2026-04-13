#!/usr/bin/env python3
"""
Smoke tests for Super Z wave launcher.
Run: python -m pytest tests/test_wave_launcher.py -v
     or: python tests/test_wave_launcher.py
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vessel" / "tools"))

import wave_launcher


class TestWaveParsing(unittest.TestCase):
    """Test task parsing."""

    def test_parse_single_task(self):
        """Single task is parsed correctly."""
        tasks = wave_launcher.parse_tasks("audit the runtime")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "audit the runtime")
        self.assertEqual(tasks[0]["wave"], 1)

    def test_parse_multiple_tasks(self):
        """Multiple comma-separated tasks are parsed."""
        tasks = wave_launcher.parse_tasks("task one, task two, task three")
        self.assertEqual(len(tasks), 3)

    def test_parse_trims_whitespace(self):
        """Leading/trailing whitespace is trimmed."""
        tasks = wave_launcher.parse_tasks("  task a  ,  task b  ")
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "task a")

    def test_parse_empty_string(self):
        """Empty string returns no tasks."""
        tasks = wave_launcher.parse_tasks("")
        self.assertEqual(len(tasks), 0)

    def test_parse_dependency_syntax_raw(self):
        """Tasks with ::dep syntax are parsed as raw strings (deps extracted later by plan)."""
        # parse_tasks splits by comma — "::" syntax is handled by plan(), not parse_tasks()
        tasks = wave_launcher.parse_tasks("task a, task b::1")
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "task a")
        self.assertEqual(tasks[1]["description"], "task b::1")
        # Dependencies are empty at parse time — plan() extracts them
        self.assertEqual(tasks[1]["dependencies"], [])


class TestWaveAssignment(unittest.TestCase):
    """Test wave number assignment."""

    def test_independent_tasks_same_wave(self):
        """Tasks with no dependencies all go in wave 1."""
        tasks = [
            {"id": 1, "dependencies": [], "wave": 1},
            {"id": 2, "dependencies": [], "wave": 1},
            {"id": 3, "dependencies": [], "wave": 1},
        ]
        result = wave_launcher.assign_waves(tasks)
        waves = {t["wave"] for t in result}
        self.assertEqual(waves, {1})

    def test_dependent_task_next_wave(self):
        """Task depending on wave 1 goes in wave 2."""
        tasks = [
            {"id": 1, "dependencies": [], "wave": 1},
            {"id": 2, "dependencies": [1], "wave": 1},
        ]
        result = wave_launcher.assign_waves(tasks)
        self.assertEqual(result[0]["wave"], 1)
        self.assertEqual(result[1]["wave"], 2)

    def test_chain_dependency(self):
        """Chain dependency a→b→c assigns waves 1,2,3."""
        tasks = [
            {"id": 1, "dependencies": [], "wave": 1},
            {"id": 2, "dependencies": [1], "wave": 1},
            {"id": 3, "dependencies": [2], "wave": 1},
        ]
        result = wave_launcher.assign_waves(tasks)
        self.assertEqual(result[0]["wave"], 1)
        self.assertEqual(result[1]["wave"], 2)
        self.assertEqual(result[2]["wave"], 3)


class TestWaveStatus(unittest.TestCase):
    """Test wave status reporting."""

    def test_status_no_state(self):
        """Status returns error code when no state file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(wave_launcher, 'WAVE_STATE_PATH', Path(tmpdir) / "nonexistent.json"):
                result = wave_launcher.status([])
                self.assertEqual(result, 1)


class TestWavePlan(unittest.TestCase):
    """Test wave planning."""

    def test_plan_no_args(self):
        """Plan without arguments returns error."""
        result = wave_launcher.plan([])
        self.assertEqual(result, 1)

    def test_plan_creates_state_file(self):
        """Plan creates a wave-state.json file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "wave-state.json"
            with patch.object(wave_launcher, 'WAVE_STATE_PATH', state_path):
                wave_launcher.plan(["plan", "task a, task b, task c"])
                self.assertTrue(state_path.exists())
                with open(state_path) as f:
                    state = json.load(f)
                self.assertEqual(state["total_tasks"], 3)
                self.assertIn("1", state["waves"])


if __name__ == "__main__":
    unittest.main()
