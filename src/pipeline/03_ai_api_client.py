#!/usr/bin/env python3
"""
03_ai_api_client.py

Rolle im Projekt:
Dieses Skript ist der API-Teil.
Es liest ein Event-JSON, sendet es an die OpenAI Responses API und speichert die strukturierte Antwort.

Sicherheit:
Der API-Key steht NICHT im Code.
Er wird aus der Umgebungsvariable OPENAI_API_KEY gelesen.
Beispiel: OPENAI_API_KEY=****
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

import requests

DEFAULT_ENDPOINT = "https://api.openai.com/v1/responses"

OUTPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "attack_type": {
            "type": "string",
            "enum": [
                "benign",
                "brute_force",
                "ddos",
                "credential_stuffing",
                "malware",
                "ransomware",
                "data_exfiltration",
                "misconfiguration",
                "unknown"
            ]
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "explanation": {"type": "string"},
        "recommended_next_steps": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["attack_type", "confidence", "explanation", "recommended_next_steps"],
    "additionalProperties": False
}


def build_payload(model: str, event: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "Du bist SOC-Analyst. Klassifiziere das gelieferte JSON-Event. "
        "Nutze nur die gelieferten Daten. Wenn die Hinweise nicht ausreichen, nutze attack_type='unknown'. "
        "Antworte ausschließlich im vorgegebenen JSON-Schema."
    )

    return {
        "model": model,
        "store": False,
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Event JSON:\n" + json.dumps(event, ensure_ascii=False)}
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "attack_classification",
                "strict": True,
                "schema": OUTPUT_SCHEMA
            }
        }
    }


def extract_response(response_json: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(response_json.get("output_text"), str):
        return json.loads(response_json["output_text"])

    for item in response_json.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") == "output_text":
                return json.loads(content["text"])

    raise ValueError("Keine strukturierte KI-Antwort gefunden.")


def call_openai(event: Dict[str, Any], model: str, timeout: int) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY fehlt. Beispiel: $env:OPENAI_API_KEY='****'")

    payload = build_payload(model, event)
    response = requests.post(
        DEFAULT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=timeout
    )

    if not response.ok:
        print("OpenAI API Fehler:", response.status_code)
        print(response.text)
    response.raise_for_status()
    return extract_response(response.json())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Event-JSON")
    parser.add_argument("--output", required=True, help="KI-Ergebnis JSON")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    event = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    result = call_openai(event, args.model, args.timeout)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] KI-Ergebnis gespeichert: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
