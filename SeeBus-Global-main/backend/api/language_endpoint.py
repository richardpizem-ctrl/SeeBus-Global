import os
import json
from flask import Blueprint, jsonify, request

language_bp = Blueprint("language", __name__)

LOCALES_PATH = "backend/locales"


def load_translations(lang):
    """Načíta jazykový JSON súbor. Ak neexistuje, použije EN."""
    path = os.path.join(LOCALES_PATH, f"{lang}.json")

    if not os.path.exists(path):
        path = os.path.join(LOCALES_PATH, "en.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@language_bp.route("/languages", methods=["GET"])
def get_languages():
    """Vráti zoznam dostupných jazykov podľa súborov v /locales."""
    languages = []

    for filename in os.listdir(LOCALES_PATH):
        if filename.endswith(".json"):
            lang_code = filename.replace(".json", "")
            languages.append(lang_code)

    return jsonify({"languages": sorted(languages)})


@language_bp.route("/translate", methods=["GET"])
def translate_preview():
    """
    Test endpoint:
    /api/translate?lang=sk&state=arriving&route=24&stop=Radvaň
    """
    lang = request.args.get("lang", "en")
    state = request.args.get("state", "arriving")
    route = request.args.get("route", "0")
    stop = request.args.get("stop", "Unknown stop")

    translations = load_translations(lang)

    if state not in translations:
        return jsonify({"error": "Unknown state"}), 400

    text = translations[state].format(route=route, stop=stop)

    return jsonify({
        "lang": lang,
        "state": state,
        "text": text
    })
