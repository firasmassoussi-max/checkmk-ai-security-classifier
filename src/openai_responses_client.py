#!/usr/bin/env python3
"""
openai_responses_client.py

Kleiner API-Client für die OpenAI Responses API.
Der API-Key wird aus der Umgebungsvariable OPENAI_API_KEY gelesen.
Im Code steht niemals ein echter Key.
"""
from __future__ import annotations

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


def build_payload(event: Dict[str, Any], model: str = "gpt-4o-mini") -> Dict[str, Any]:
    system_msg = (
        "Du bist SOC-Analyst. Klassifiziere das JSON-Event nur anhand der gelieferten Features. "
        "Wenn die Informationen nicht reichen, gib attack_type='unknown' zurück. "
        "Antworte ausschließlich im vorgegebenen JSON-Schema."
    )
    return {
        "model": model,
        "store": False,
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


def call_openai(payload: Dict[str, Any], endpoint: str = DEFAULT_ENDPOINT, timeout: int = 30) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt. Beispiel: $env:OPENAI_API_KEY='****'")

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    if not response.ok:
        print("OpenAI ERROR:", response.status_code)
        print(response.text)
    response.raise_for_status()
    return response.json()


def extract_output(response_json: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(response_json.get("output_text"), str):
        return json.loads(response_json["output_text"])

    for item in response_json.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                return json.loads(content["text"])

    raise ValueError("Keine strukturierte output_text-Antwort gefunden.")
