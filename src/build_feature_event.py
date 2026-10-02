#!/usr/bin/env python3
"""
build_feature_event.py

Liest ein Raw-Samples-JSON und baut daraus ein datensparsames Feature-Event.
Das simuliert den Schritt, der später durch Checkmk-Metriken automatisiert werden könnte.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from feature_engineering import calculate_feature_set


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def build_event(raw: Dict[str, Any]) -> Dict[str, Any]:
    samples = raw.get("samples", {})
    return {
        "source": raw.get("source", "checkmk_or_synthetic"),
        "host": raw.get("host", "host-redacted"),
        "service": raw.get("service", "monitoring-feature-event"),
        "state": raw.get("state", "UNKNOWN"),
        "window_sec": raw.get("window_sec", 300),
        "features": calculate_feature_set(samples),
        "hints": raw.get("hints", {}),
        "note": "Datensparsames Feature-JSON: keine Rohlogs, keine echten User, keine echten IPs.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Raw samples JSON")
    parser.add_argument("--output", "-o", required=True, help="Output feature event JSON")
    args = parser.parse_args()

    raw = load_json(args.input)
    event = build_event(raw)
    Path(args.output).write_text(json.dumps(event, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(event, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
