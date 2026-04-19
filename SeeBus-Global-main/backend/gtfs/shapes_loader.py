"""
SHAPES LOADER
-------------
Načíta GTFS shapes.txt a vráti:
- shape_id → list bodov (lat, lon, sequence)
zoradené podľa shape_pt_sequence.

Používa sa na vykreslenie trasy linky.
"""

import csv
from pathlib import Path
from typing import Dict, List, Any


def load_shapes(gtfs_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    """
    Načíta shapes.txt a vráti:
    {
        "shape_id_1": [
            {"lat": ..., "lon": ..., "seq": ...},
            ...
        ],
        ...
    }
    """

    shapes_file = gtfs_dir / "shapes.txt"

    if not shapes_file.exists():
        print("⚠ shapes.txt nenájdený!")
        return {}

    shapes: Dict[str, List[Dict[str, Any]]] = {}

    with shapes_file.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            shape_id = row.get("shape_id")
            if not shape_id:
                continue

            lat = float(row.get("shape_pt_lat", 0))
            lon = float(row.get("shape_pt_lon", 0))
            seq = int(row.get("shape_pt_sequence", 0))

            if shape_id not in shapes:
                shapes[shape_id] = []

            shapes[shape_id].append({
                "lat": lat,
                "lon": lon,
                "seq": seq
            })

    # ⭐ Zoradiť body podľa sequence
    for sid in shapes:
        shapes[sid].sort(key=lambda x: x["seq"])

    return shapes
