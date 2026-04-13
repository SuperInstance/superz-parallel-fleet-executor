#!/usr/bin/env python3
"""
Smoke tests for Super Z boot script.
Run: python -m pytest tests/test_boot.py -v
     or: python tests/test_boot.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add vessel/tools to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vessel" / "tools"))

import boot


class TestBootConfig(unittest.TestCase):
    """Test config validation."""

    def test_missing_config_returns_none(self):
        """boot.read_config returns None when config.json doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(boot, 'CONFIG_PATH', Path(tmpdir) / "nonexistent.json"):
                result = boot.read_config()
                self.assertIsNone(result)

    def test_valid_config_passes_validation(self):
        """A well-formed config passes all validation checks."""
        good_config = {
            "agent_name": "Test Agent",
            "model": {
                "api_key": "sk-test-12345",
                "api_url": "https://api.example.com/v1/chat",
                "model_id": "test-model"
            }
        }
        errors = boot.validate_config(good_config)
        self.assertEqual(errors, [])

    def test_missing_api_key_fails(self):
        """Config without api_key fails validation."""
        bad_config = {
            "model": {
                "api_url": "https://api.example.com",
                "model_id": "test-model"
            }
        }
        errors = boot.validate_config(bad_config)
        self.assertTrue(any("api_key" in e for e in errors))

    def test_placeholder_api_key_fails(self):
        """Config with placeholder api_key fails validation."""
        bad_config = {
            "model": {
                "api_key": "YOUR_API_KEY_HERE",
                "api_url": "https://api.example.com",
                "model_id": "test-model"
            }
        }
        errors = boot.validate_config(bad_config)
        self.assertTrue(any("placeholder" in e.lower() for e in errors))

    def test_missing_model_id_fails(self):
        """Config without model_id fails validation."""
        bad_config = {
            "model": {
                "api_key": "sk-test-12345",
                "api_url": "https://api.example.com"
            }
        }
        errors = boot.validate_config(bad_config)
        self.assertTrue(any("model_id" in e for e in errors))


class TestBootScan(unittest.TestCase):
    """Test directive scanning."""

    def test_scan_empty_directory(self):
        """Empty from-fleet/ returns no directives."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(boot, 'FROM_FLEET_DIR', Path(tmpdir)):
                result = boot.scan_directives()
                self.assertEqual(result, [])

    def test_scan_excludes_readme(self):
        """README.md in from-fleet/ is excluded from directives."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fleet_dir = Path(tmpdir)
            (fleet_dir / "README.md").write_text("protocol docs")
            (fleet_dir / "directive-001.md").write_text("directive content")
            with patch.object(boot, 'FROM_FLEET_DIR', fleet_dir):
                result = boot.scan_directives()
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["file"], "directive-001.md")

    def test_scan_finds_directives(self):
        """Directive files are found and parsed correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fleet_dir = Path(tmpdir)
            (fleet_dir / "directive-001.md").write_text("task one")
            (fleet_dir / "priority-001.md").write_text("urgent task")
            (fleet_dir / "health-check-001.md").write_text("health check")
            with patch.object(boot, 'FROM_FLEET_DIR', fleet_dir):
                result = boot.scan_directives()
                self.assertEqual(len(result), 3)

    def test_scan_ignores_hidden_files(self):
        """Hidden files (starting with .) are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fleet_dir = Path(tmpdir)
            (fleet_dir / ".hidden").write_text("hidden")
            (fleet_dir / "directive-001.md").write_text("visible")
            with patch.object(boot, 'FROM_FLEET_DIR', fleet_dir):
                result = boot.scan_directives()
                self.assertEqual(len(result), 1)

    def test_scan_reports_file_size(self):
        """Directive entries include file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fleet_dir = Path(tmpdir)
            content = "x" * 100
            (fleet_dir / "directive-001.md").write_text(content)
            with patch.object(boot, 'FROM_FLEET_DIR', fleet_dir):
                result = boot.scan_directives()
                self.assertEqual(result[0]["size_bytes"], 100)


class TestBootHealth(unittest.TestCase):
    """Test health response generation."""

    def test_health_response_structure(self):
        """Health response has all required fields."""
        config = {
            "agent_name": "Test Agent",
            "model": {"model_id": "test-model"}
        }
        response = boot.generate_health_response(config)
        self.assertEqual(response["agent"], "Test Agent")
        self.assertEqual(response["status"], "active")
        self.assertEqual(response["model"], "test-model")
        self.assertIn("tasks_in_progress", response)
        self.assertIn("blockers", response)
        self.assertIn("needs", response)
        self.assertIn("meta", response)

    def test_health_shows_no_directives(self):
        """Health response shows empty tasks when no directives exist."""
        config = {"agent_name": "Test", "model": {"model_id": "m"}}
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(boot, 'FROM_FLEET_DIR', Path(tmpdir)):
                with patch.object(boot, 'FOR_FLEET_DIR', Path(tmpdir)):
                    response = boot.generate_health_response(config)
                    self.assertEqual(response["tasks_in_progress"], [])
                    self.assertEqual(response["last_directive_received"], "never")


class TestSessionCounting(unittest.TestCase):
    """Test session report counting."""

    def test_count_empty_directory(self):
        """Empty for-fleet/ returns 0 sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(boot, 'FOR_FLEET_DIR', Path(tmpdir)):
                self.assertEqual(boot.count_session_reports(), 0)

    def test_count_session_files(self):
        """Counts files starting with 'session-' in for-fleet/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fleet_dir = Path(tmpdir)
            (fleet_dir / "session-001.md").write_text("report 1")
            (fleet_dir / "session-002.md").write_text("report 2")
            (fleet_dir / "other-file.md").write_text("not a session")
            (fleet_dir / "README.md").write_text("docs")
            with patch.object(boot, 'FOR_FLEET_DIR', fleet_dir):
                self.assertEqual(boot.count_session_reports(), 2)


if __name__ == "__main__":
    unittest.main()
