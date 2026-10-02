#!/usr/bin/env python3
"""
batch_demo_runner.py

Führt mehrere Demo-JSON-Dateien nacheinander gegen die Klassifikation aus.
So kann man im Video oder im Gespräch schnell zeigen, dass die Pipeline reproduzierbar ist.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from openai_responses_client import build_payload, call_openai, extract_output


def load_json(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True, help="JSON input files")
    parser.add_argument("--outdir", default="results", help="Output directory")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary: List[Dict] = []

    for input_file in args.inputs:
        path = Path(input_file)
        event = load_json(path)
        payload = build_payload(event, model=args.model)
        response = call_openai(payload)
        result = extract_output(response)

        output_path = outdir / f"{path.stem}_result.json"
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

        summary.append({
            "input": str(path),
            "output": str(output_path),
            "attack_type": result.get("attack_type"),
            "confidence": result.get("confidence"),
        })

    summary_path = outdir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
