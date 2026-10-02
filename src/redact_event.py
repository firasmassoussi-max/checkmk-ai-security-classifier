#!/usr/bin/env python3
"""
redact_event.py

Entfernt oder ersetzt sensible Felder aus einem JSON-Event.
Ziel: Datensparsamkeit vor dem Senden an eine externe API.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

SENSITIVE_KEYS = {
    "ip",
    "source_ip",
    "destination_ip",
    "src_ip",
    "dst_ip",
    "username",
    "user",
    "hostname",
    "email",
    "filepath",
    "file_path",
    "command_line",
}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: Dict[str, Any] = {}
        for key, val in value.items():
            if key.lower() in SENSITIVE_KEYS:
                cleaned[key] = "REDACTED"
            else:
                cleaned[key] = redact(val)
        return cleaned
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8-sig") as f:
        event = json.load(f)

    cleaned = redact(event)
    Path(args.output).write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(cleaned, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
