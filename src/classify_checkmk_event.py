#!/usr/bin/env python3
"""
classify_checkmk_event.py

Einfaches Skript:
- liest eine JSON-Datei
- sendet sie an die OpenAI Responses API
- speichert die strukturierte Antwort als JSON

API-Key wird NICHT im Code gespeichert.
PowerShell-Beispiel:
$env:OPENAI_API_KEY="****"
"""
from __future__ import annotations

import argparse
import json
import os
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
                "unknown",
            ],
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "explanation": {"type": "string"},
        "recommended_next_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["attack_type", "confidence", "explanation", "recommended_next_steps"],
    "additionalProperties": False,
}


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def build_request(model: str, event: Dict[str, Any], store: bool) -> Dict[str, Any]:
    system_msg = (
        "Du bist SOC-Analyst. Klassifiziere das Ereignis ausschließlich anhand des JSON-Events. "
        "Wenn die Informationen nicht reichen, gib attack_type='unknown' aus. "
        "Gib eine kurze Erklärung und konkrete Next Steps."
    )
    return {
        "model": model,
        "store": store,
        "input": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": "Event JSON:\n" + json.dumps(event, ensure_ascii=False)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "attack_classification",
                "strict": True,
                "schema": OUTPUT_SCHEMA,
            }
        },
    }


def call_openai(endpoint: str, api_key: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    r = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    if not r.ok:
        print("OpenAI ERROR:", r.status_code)
        print(r.text)
    r.raise_for_status()
    return r.json()


def extract_output(resp_json: Dict[str, Any]) -> Dict[str, Any]:
    for item in resp_json.get("output", []) or []:
        if item.get("type") == "message":
            for content in item.get("content", []) or []:
                if content.get("type") == "output_text":
                    return json.loads(content["text"])
    raise ValueError("Keine strukturierte KI-Antwort gefunden.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="result.json")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--endpoint", default=os.getenv("OPENAI_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--store", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY fehlt. Beispiel: $env:OPENAI_API_KEY='****'")

    event = load_json(args.input)
    request_payload = build_request(args.model, event, args.store)
    response_json = call_openai(args.endpoint, api_key, request_payload, args.timeout)
    result = extract_output(response_json)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
