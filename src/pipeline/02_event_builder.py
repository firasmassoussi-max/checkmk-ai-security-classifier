#!/usr/bin/env python3
"""
02_event_builder.py

Rolle im Projekt:
Dieses Skript nimmt gesammelte Werte entgegen und baut daraus ein datensparsames Event-JSON.
Es berechnet Kennzahlen wie Mittelwert, Median, Maximum und MAD.

Warum?
Statt komplette Rohlogs oder sensible Details an die KI zu senden, werden nur verdichtete Features übertragen.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any, Dict, List


def mad(values: List[float]) -> float:
    if not values:
        return 0.0
    med = statistics.median(values)
    return float(statistics.median([abs(v - med) for v in values]))


def summarize(values: List[float]) -> Dict[str, float | int]:
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "min": float(min(values)),
        "max": float(max(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "mad": mad(values),
    }


def build_event(collected: Dict[str, Any]) -> Dict[str, Any]:
    raw_values = collected.get("raw_values", {})
    features: Dict[str, Any] = {}

    for name, values in raw_values.items():
        if isinstance(values, list):
            numeric = [float(v) for v in values]
            features[name] = summarize(numeric)

    return {
        "source": collected.get("source", "unknown"),
        "scenario": collected.get("scenario", "unknown"),
        "host": collected.get("host", "anonymized-host"),
        "service": collected.get("service", "unknown-service"),
        "window_minutes": collected.get("window_minutes", 5),
        "features": features,
        "hints": collected.get("hints", {}),
        "privacy_note": "Datensparsam: Es werden nur aggregierte Kennzahlen übertragen, keine vollständigen Rohlogs."
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON mit simulierten Checkmk-Werten")
    parser.add_argument("--output", required=True, help="Event-JSON für KI")
    args = parser.parse_args()

    collected = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    event = build_event(collected)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Event-JSON erzeugt: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
