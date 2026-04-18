import logging
import os
import json

from .event_engine import EventEngine
from .voice_service import VoiceService
from .text_service import TextService
from .vibration_service import VibrationService

# Logger
logger = logging.getLogger("SeeBus")
logger.setLevel(logging.INFO)

LOCALES_PATH = "backend/locales"


def load_translations(lang):
    """Načíta jazykový JSON súbor. Ak neexistuje, použije EN."""
    path = os.path.join(LOCALES_PATH, f"{lang}.json")

    if not os.path.exists(path):
        path = os.path.join(LOCALES_PATH, "en.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class EventDispatcher:

    def __init__(self, stops, stop_times):
        self.engine = EventEngine(stops, stop_times)
        self.voice = VoiceService()
        self.text = TextService()
        self.vibration = VibrationService()

    def process(self, vehicle_id, vehicle, route_short_name, lang):
        """
        Spracuje jedno vozidlo a vráti všetky typy hlásení naraz.
        """

        # Načítame jazykové preklady
        translations = load_translations(lang)

        result = self.engine.process_vehicle(vehicle_id, vehicle)

        if not result:
            return None

        state, stop = result

        # TEXTOVÉ HLÁSENIE PODĽA JAZYKA
        text_msg = translations[state].format(
            route=route_short_name,
            stop=stop.stop_name
        )

        # VOICE HLÁSENIE (zatiaľ bez jazykovej podpory)
        voice_msg = self.voice.generate_announcement(
            state,
            route_short_name,
            stop.stop_name
        )

        # VIBRÁCIA
        vibration_pattern = self.vibration.generate_vibration_pattern(state)

        # -----------------------------
        # LOGGING
        # -----------------------------
        logger.info(
            f"[{state}] lang={lang} "
            f"stop={stop.stop_name} "
            f"voice='{voice_msg}' "
            f"text='{text_msg}' "
            f"vibration={vibration_pattern}"
        )

        # Vrátime jednotný objekt pre frontend
        return {
            "state": state,
            "stop_id": stop.stop_id,
            "stop_name": stop.stop_name,
            "voice": voice_msg,
            "text": text_msg,
            "vibration": vibration_pattern,
            "lang": lang
        }
