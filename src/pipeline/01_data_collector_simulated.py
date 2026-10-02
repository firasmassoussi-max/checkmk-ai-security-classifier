#!/usr/bin/env python3
"""
01_data_collector_simulated.py

Rolle im Projekt:
Dieses Skript simuliert den Teil, der ursprünglich von Checkmk kommen sollte.
In der echten Idee hätte Checkmk Werte wie CPU, IOwait, Netzwerk oder fehlgeschlagene Logins geliefert.
Da die direkte Checkmk-Anbindung im Projekt nicht stabil umgesetzt wurde, erzeugt dieses Skript Beispiel-Messwerte.

Wichtig:
- Kein API-Key im Code.
- Keine echten personenbezogenen Daten.
- Nur synthetische Beispielwerte für die Demonstration.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def build_simulated_checkmk_values(scenario: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()

    if scenario == "malware":
        return {
            "source": "checkmk_simulated",
            "scenario": "malware_like_resource_abuse",
            "collected_at": now,
            "host": "host-01",
            "service": "CPU + process anomaly",
            "window_minutes": 5,
            "raw_values": {
                "cpu_percent": [92, 95, 97, 98, 96, 99, 97, 98, 96, 97],
                "iowait_percent": [18, 20, 22, 21, 23, 24, 22, 25, 23, 24],
                "net_out_mbps": [6, 7, 8, 10, 15, 18, 20, 19, 17, 16],
                "process_count_new": [2, 3, 5, 7, 8, 9, 8, 10, 9, 11]
            },
            "hints": {
                "known_bad_process_matches": ["xmrig"],
                "unusual_outbound_connections": True
            }
        }

    if scenario == "credential_stuffing":
        return {
            "source": "checkmk_simulated",
            "scenario": "credential_stuffing",
            "collected_at": now,
            "host": "auth-system-01",
            "service": "Authentication anomalies",
            "window_minutes": 5,
            "raw_values": {
                "failed_logins": [10, 12, 15, 20, 18, 17, 14, 16, 19, 21],
                "successful_logins": [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                "unique_accounts": [8, 10, 12, 15, 14, 13, 12, 13, 16, 17],
                "unique_sources": [6, 8, 10, 12, 15, 14, 16, 18, 20, 22]
            },
            "hints": {
                "many_accounts_targeted": True,
                "many_sources_seen": True
            }
        }

    return {
        "source": "checkmk_simulated",
        "scenario": "cpu_alarm_unknown",
        "collected_at": now,
        "host": "server-01",
        "service": "CPU utilization",
        "window_minutes": 5,
        "raw_values": {
            "cpu_percent": [80, 84, 88, 91, 92, 90, 89, 87, 85, 83]
        },
        "hints": {}
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=["malware", "credential_stuffing", "cpu"], default="malware")
    parser.add_argument("--output", default="examples/collected_values.json")
    args = parser.parse_args()

    data = build_simulated_checkmk_values(args.scenario)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Simulierte Checkmk-Werte gespeichert: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
