class VibrationService:

    def generate_vibration_pattern(self, state):
        """
        Vráti vibračný pattern podľa stavu.
        Pattern je zoznam dĺžok vibrácií v milisekundách.
        """

        if state == "ARRIVING":
            # krátke upozornenie
            return [200, 100, 200]

        if state == "AT_STOP":
            # dlhšia vibrácia
            return [500]

        if state == "DEPARTING":
            # dvojité upozornenie
            return [300, 150, 300]

        return None
if state == "MISSED":
    return [800, 200, 800]  # silné varovanie
