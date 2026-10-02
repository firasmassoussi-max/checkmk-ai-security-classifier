#!/usr/bin/env python3
"""
feature_engineering.py

Berechnet datensparsame Kennzahlen aus Monitoring-Werten.
Diese Werte können aus Checkmk stammen oder für die Simulation als JSON vorliegen.

Berechnete Features:
- count
- min / max
- mean (Mittelwert)
- median
- p95
- stdev
- mad (Median Absolute Deviation)
"""
from __future__ import annotations

import json
import statistics
from typing import Any, Dict, List


def to_float_list(values: List[Any]) -> List[float]:
    return [float(v) for v in values if v is not None]


def mad(values: List[float]) -> float:
    if not values:
        return 0.0
    med = statistics.median(values)
    deviations = [abs(v - med) for v in values]
    return float(statistics.median(deviations))


def percentile_95(values: List[float]) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    index = int(round(0.95 * (len(values_sorted) - 1)))
    return float(values_sorted[index])


def calculate_stats(values: List[Any]) -> Dict[str, Any]:
    nums = to_float_list(values)
    if not nums:
        return {"count": 0}

    return {
        "count": len(nums),
        "min": float(min(nums)),
        "max": float(max(nums)),
        "mean": float(statistics.mean(nums)),
        "median": float(statistics.median(nums)),
        "p95": percentile_95(nums),
        "stdev": float(statistics.stdev(nums)) if len(nums) > 1 else 0.0,
        "mad": mad(nums),
    }


def calculate_feature_set(samples: Dict[str, List[Any]]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for name, values in samples.items():
        if isinstance(values, list):
            result[name] = calculate_stats(values)
    return result


if __name__ == "__main__":
    demo_samples = {
        "cpu_pct": [92, 95, 97, 99, 96],
        "iowait_pct": [10, 15, 20, 22, 19],
        "net_out_mbps": [5, 8, 9, 20, 18],
    }
    print(json.dumps(calculate_feature_set(demo_samples), indent=2, ensure_ascii=False))
