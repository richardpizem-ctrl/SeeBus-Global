"""
GTFS CACHE LAYER
----------------
Tento modul načíta statické GTFS dáta (routes, trips, stop_times, shapes)
iba raz pri štarte backendu a drží ich v pamäti.

Výhody:
- rýchlejší štart stream endpointu
- žiadne opakované čítanie CSV súborov
- jednotný zdroj pravdy pre celý backend
"""

from pathlib import Path
from typing import Dict, List, Any

from backend.gtfs.static_loader import (
    load_routes,
    load_trips,
    load_stop_times,
)

# ⭐ shapes loader (KROK 18)
from backend.gtfs.shapes_loader import load_shapes


# ⭐ CESTA K STATIC GTFS
GTFS_DIR = Path("backend/gtfs/static")


# ⭐ CACHE PRE ROUTES, TRIPS, STOP_TIMES, SHAPES
_routes_cache: Dict[str, Dict[str, Any]] | None = None
_trips_cache: Dict[str, Dict[str, Any]] | None = None
_stop_times_cache: Dict[str, List[Dict[str, Any]]] | None = None
_shapes_cache: Dict[str, List[Dict[str, Any]]] | None = None


def load_cache_if_needed() -> None:
    """
    Načíta všetky GTFS dáta do pamäte, ak ešte nie sú načítané.
    """
    global _routes_cache, _trips_cache, _stop_times_cache, _shapes_cache

    if _routes_cache is None:
        _routes_cache = load_routes(GTFS_DIR)

    if _trips_cache is None:
        _trips_cache = load_trips(GTFS_DIR)

    if _stop_times_cache is None:
        _stop_times_cache = load_stop_times(GTFS_DIR)

    # ⭐ shapes (NOVÉ)
    if _shapes_cache is None:
        _shapes_cache = load_shapes(GTFS_DIR)


# ⭐ PUBLIC API — tieto funkcie používa celý backend

def get_routes() -> Dict[str, Dict[str, Any]]:
    load_cache_if_needed()
    return _routes_cache


def get_trips() -> Dict[str, Dict[str, Any]]:
    load_cache_if_needed()
    return _trips_cache


def get_stop_times() -> Dict[str, List[Dict[str, Any]]]:
    load_cache_if_needed()
    return _stop_times_cache


def get_shapes() -> Dict[str, List[Dict[str, Any]]]:
    """
    Vráti shape_id → zoznam bodov (lat, lon, seq)
    """
    load_cache_if_needed()
    return _shapes_cache
