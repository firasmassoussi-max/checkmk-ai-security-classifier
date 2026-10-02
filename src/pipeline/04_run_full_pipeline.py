#!/usr/bin/env python3
"""
04_run_full_pipeline.py

Rolle im Projekt:
Dieses Skript verbindet alle Bausteine:
1. Daten sammeln/simulieren
2. Event-JSON bauen
3. Event an KI-API senden
4. Ergebnis speichern

Damit sieht man den vollständigen Ablauf der Demo-Pipeline.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("\n> " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=["malware", "credential_stuffing", "cpu"], default="malware")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    collected = Path("examples/collected_values.json")
    event = Path("examples/event_from_features.json")
    result = Path("examples/result_from_ai.json")

    run([sys.executable, "src/pipeline/01_data_collector_simulated.py", "--scenario", args.scenario, "--output", str(collected)])
    run([sys.executable, "src/pipeline/02_event_builder.py", "--input", str(collected), "--output", str(event)])
    run([sys.executable, "src/pipeline/03_ai_api_client.py", "--input", str(event), "--output", str(result), "--model", args.model])

    print("\n[OK] Vollständige Pipeline erfolgreich ausgeführt.")
    print(f"Ergebnis: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
