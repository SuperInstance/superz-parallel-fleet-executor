#!/usr/bin/env python3
"""
Super Z Boot Script — Assembles agent runtime from vessel components.

Usage:
    python vessel/tools/boot.py [--validate] [--scan] [--health]

Options:
    --validate    Validate config.json exists and has required fields
    --scan        Scan from-fleet/ for new directives
    --health      Generate health response JSON
    --version     Print version and exit

This script is the entry point for booting the agent. It:
1. Reads vessel/lighthouse/config.json for runtime configuration
2. Validates the config has required fields
3. Scans from-fleet/ for pending directives
4. Generates a health response if requested
5. Reports what the agent should do next
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VESSEL_DIR = REPO_ROOT / "vessel"
CONFIG_PATH = VESSEL_DIR / "lighthouse" / "config.json"
CAPABILITY_PATH = REPO_ROOT / "CAPABILITY.toml"
ONBOARDING_PATH = REPO_ROOT / "agent-personallog" / "onboarding.md"
FROM_FLEET_DIR = REPO_ROOT / "from-fleet"
FOR_FLEET_DIR = REPO_ROOT / "for-fleet"
HEALTH_RESPONSE_PATH = VESSEL_DIR / "lighthouse" / "health-response.json"

REQUIRED_CONFIG_FIELDS = [
    ("model.api_key", str),
    ("model.api_url", str),
    ("model.model_id", str),
]


def read_config():
    """Read and parse config.json."""
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found at {CONFIG_PATH}")
        print(f"  Copy vessel/lighthouse/config.example.json to vessel/lighthouse/config.json")
        print(f"  Fill in your API key and model URL.")
        return None
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def validate_config(config):
    """Validate config has all required fields."""
    errors = []
    for field_path, field_type in REQUIRED_CONFIG_FIELDS:
        parts = field_path.split(".")
        obj = config
        for part in parts:
            if isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                errors.append(f"Missing required field: {field_path}")
                break
        else:
            if not isinstance(obj, field_type):
                errors.append(f"Field {field_path} should be {field_type.__name__}, got {type(obj).__name__}")
            if field_path == "model.api_key" and obj == "YOUR_API_KEY_HERE":
                errors.append(f"Field model.api_key is still set to placeholder value")
    return errors


def scan_directives():
    """Scan from-fleet/ for pending directives."""
    if not FROM_FLEET_DIR.exists():
        return []
    directives = []
    for f in sorted(FROM_FLEET_DIR.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            directives.append({
                "file": f.name,
                "path": str(f),
                "modified": mtime.isoformat(),
                "size_bytes": stat.st_size
            })
    return directives


def count_session_reports():
    """Count session reports in for-fleet/."""
    if not FOR_FLEET_DIR.exists():
        return 0
    count = 0
    for f in FOR_FLEET_DIR.iterdir():
        if f.is_file() and f.name.startswith("session-"):
            count += 1
    return count


def generate_health_response(config):
    """Generate a health response JSON."""
    directives = scan_directives()
    session_count = count_session_reports()

    response = {
        "agent": config.get("agent_name", "Super Z"),
        "status": "active",
        "session": session_count,
        "model": config.get("model", {}).get("model_id", "unknown"),
        "tasks_in_progress": [d["file"] for d in directives if "directive" in d["file"].lower()],
        "last_push": datetime.now(timezone.utc).isoformat(),
        "last_directive_received": directives[0]["modified"] if directives else "never",
        "blockers": [],
        "needs": [],
        "meta": {
            "directives_pending": len(directives),
            "session_reports": session_count,
            "config_valid": True
        }
    }

    return response


def validate(args):
    """Run validation."""
    config = read_config()
    if config is None:
        return False
    errors = validate_config(config)
    if errors:
        print("CONFIG VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False
    print("CONFIG VALIDATION PASSED")
    print(f"  Model: {config['model']['model_id']}")
    print(f"  API URL: {config['model']['api_url']}")
    print(f"  Max Wave Size: {config.get('runtime', {}).get('max_wave_size', 8)}")
    return True


def scan(args):
    """Scan for directives."""
    directives = scan_directives()
    if not directives:
        print("No pending directives in from-fleet/")
    else:
        print(f"Found {len(directives)} directive(s) in from-fleet/:")
        for d in directives:
            print(f"  - {d['file']} ({d['size_bytes']} bytes, modified {d['modified']})")
    return directives


def health(args):
    """Generate health response."""
    config = read_config()
    if config is None:
        print("Cannot generate health response: config not found")
        return
    response = generate_health_response(config)
    HEALTH_RESPONSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HEALTH_RESPONSE_PATH, "w") as f:
        json.dump(response, f, indent=2)
    print(f"Health response written to {HEALTH_RESPONSE_PATH}")
    print(json.dumps(response, indent=2))


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    if "--version" in args:
        print("Super Z Boot Script v1.0.0")
        return 0

    if "--validate" in args:
        return 0 if validate(args) else 1

    if "--scan" in args:
        scan(args)
        return 0

    if "--health" in args:
        health(args)
        return 0

    # Default: full boot sequence
    print("=== Super Z Boot Sequence ===")
    print()

    # Step 1: Validate config
    print("[1/4] Validating configuration...")
    config = read_config()
    if config is None:
        print("  SKIPPED: No config found. Using defaults.")
    else:
        errors = validate_config(config)
        if errors:
            print("  WARNING: Config has issues:")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"  OK: Model={config['model']['model_id']}")

    # Step 2: Check onboarding
    print("[2/4] Checking onboarding...")
    if ONBOARDING_PATH.exists():
        print(f"  OK: onboarding.md found ({ONBOARDING_PATH.stat().st_size} bytes)")
    else:
        print("  WARNING: onboarding.md not found. Agent will start cold.")

    # Step 3: Scan directives
    print("[3/4] Scanning directives...")
    directives = scan_directives()
    print(f"  Found {len(directives)} pending directive(s)")

    # Step 4: Session history
    print("[4/4] Session history...")
    sessions = count_session_reports()
    print(f"  {sessions} previous session report(s)")

    print()
    print("=== Boot Complete ===")
    if config is None:
        print("ACTION REQUIRED: Configure vessel/lighthouse/config.json")
    elif directives:
        print(f"ACTION: Process {len(directives)} pending directive(s)")
    else:
        print("STATUS: Ready. Waiting for directives in from-fleet/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
