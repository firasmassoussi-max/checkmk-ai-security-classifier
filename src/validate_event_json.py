#!/usr/bin/env python3
"""
validate_event_json.py

Einfache Validierung für Demo-Events.
Prüft, ob die wichtigsten Felder vorhanden sind.
"""
from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

REQUIRED_TOP_LEVEL = ["source", "host", "service", "state"]


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def validate(event: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for field in REQUIRED_TOP_LEVEL:
        if field not in event:
            errors.append(f"Pflichtfeld fehlt: {field}")

    if "features" not in event and "metrics" not in event:
        errors.append("Es fehlt features oder metrics.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    args = parser.parse_args()

    event = load_json(args.input)
    errors = validate(event)

    if errors:
        print("JSON ist NICHT gültig für die Demo:")
        for err in errors:
            print("-", err)
        return 1

    print("JSON ist gültig für die Demo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
