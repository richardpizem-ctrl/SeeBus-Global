from .event_engine import EventEngine
from .voice_service import VoiceService
from .text_service import TextService
from .vibration_service import VibrationService


class EventDispatcher:

    def __init__(self, stops, stop_times):
        self.engine = EventEngine(stops, stop_times)
        self.voice = VoiceService()
        self.text = TextService()
        self.vibration = VibrationService()

    def process(self, vehicle_id, vehicle, route_short_name):
        """
        Spracuje jedno vozidlo a vráti všetky typy hlásení naraz.
        """

        result = self.engine.process_vehicle(vehicle_id, vehicle)

        if not result:
            return None

        state, stop = result

        # Vygenerujeme všetky typy hlásení
        voice_msg = self.voice.generate_announcement(
            state,
            route_short_name,
            stop.stop_name
        )

        text_msg = self.text.generate_text_message(
            state,
            route_short_name,
            stop.stop_name
        )

        vibration_pattern = self.vibration.generate_vibration_pattern(state)

        # Vrátime jednotný objekt pre frontend
        return {
            "state": state,
            "stop_id": stop.stop_id,
            "stop_name": stop.stop_name,
            "voice": voice_msg,
            "text": text_msg,
            "vibration": vibration_pattern
        }
