#!/usr/bin/env python3
"""
checkmk_ai_classifier.py

Simulation einer KI-gestuetzten Checkmk/Security-Event-Klassifikation.

Ablauf:
1. JSON-Event lesen
2. optional aus Messwertlisten Features berechnen (Mean, Median, Max, MAD usw.)
3. Event an OpenAI Responses API senden
4. strukturierte JSON-Antwort speichern

Wichtig:
- Kein API-Key im Code.
- API-Key wird als Umgebungsvariable OPENAI_API_KEY gesetzt.
- Beispiel in PowerShell: $env:OPENAI_API_KEY="****"
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
from typing import Any, Dict, List

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
    # utf-8-sig verhindert Fehler durch UTF-8 BOM am Dateianfang.
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def mad(values: List[float]) -> float:
    """Median Absolute Deviation als robuste Streuungskennzahl."""
    if not values:
        return 0.0
    med = statistics.median(values)
    return float(statistics.median([abs(x - med) for x in values]))


def percentile_95(values: List[float]) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = round(0.95 * (len(sorted_values) - 1))
    return float(sorted_values[index])


def calc_stats(values: List[float]) -> Dict[str, Any]:
    """Berechnet Kennzahlen fuer eine Messwertliste."""
    if not values:
        return {"count": 0}

    return {
        "count": len(values),
        "min": float(min(values)),
        "max": float(max(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "p95": percentile_95(values),
        "mad": mad(values),
        "stdev": float(statistics.stdev(values)) if len(values) > 1 else 0.0,
    }


def build_feature_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nimmt ein JSON-Event und erzeugt ein kompaktes Feature-Event.

    Wenn das Input-JSON ein Feld "samples" enthaelt, werden daraus Kennzahlen berechnet.
    Wenn keine Samples existieren, wird das Event unveraendert bzw. minimal normalisiert weitergegeben.
    """
    samples = raw_event.get("samples")
    if not isinstance(samples, dict):
        return raw_event

    features: Dict[str, Any] = {}
    for name, raw_values in samples.items():
        if isinstance(raw_values, list):
            numeric_values = [float(v) for v in raw_values]
            features[name] = calc_stats(numeric_values)

    return {
        "source": raw_event.get("source", "checkmk_or_synthetic"),
        "meta": raw_event.get("meta", {}),
        "window_sec": raw_event.get("window_sec", 300),
        "features": features,
        "hints": raw_event.get("hints", {}),
    }


def build_request(model: str, event: Dict[str, Any], store: bool) -> Dict[str, Any]:
    system_message = (
        "Du bist ein SOC-Analyst. Klassifiziere das Ereignis nur anhand des gelieferten JSON-Events. "
        "Wenn die Hinweise nicht ausreichen, gib attack_type='unknown' aus. "
        "Nutze die Kennzahlen wie Mean, Median, Max, MAD, Dauer ueber Schwellwerten und Hinweise aus 'hints'. "
        "Antwort immer im vorgegebenen JSON-Schema."
    )

    return {
        "model": model,
        "store": store,
        "input": [
            {"role": "system", "content": system_message},
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


def extract_structured_output(response_json: Dict[str, Any]) -> Dict[str, Any]:
    # Falls eine Library direkt output_text liefert.
    if isinstance(response_json.get("output_text"), str):
        return json.loads(response_json["output_text"])

    # REST Responses API: output -> message -> content -> output_text
    for item in response_json.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                return json.loads(content["text"])

    raise ValueError("Keine strukturierte KI-Antwort gefunden.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Pfad zur JSON-Eingabedatei")
    parser.add_argument("--output", "-o", default="result.json", help="Pfad zur Ergebnisdatei")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--endpoint", default=os.getenv("OPENAI_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--timeout", type=int, default=int(os.getenv("OPENAI_TIMEOUT", "20")))
    parser.add_argument("--store", action="store_true", help="Antwort bei OpenAI speichern (standard: False)")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY fehlt. Beispiel: $env:OPENAI_API_KEY='****'")

    raw_event = load_json(args.input)
    feature_event = build_feature_event(raw_event)
    request_payload = build_request(args.model, feature_event, args.store)
    response_json = call_openai(args.endpoint, api_key, request_payload, args.timeout)
    result = extract_structured_output(response_json)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    save_json(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
