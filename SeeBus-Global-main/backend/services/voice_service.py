class VoiceService:

    def generate_announcement(self, state, route_short_name, stop_name):
        """
        Vytvorí text hlásenia podľa stavu.
        """

        if state == "ARRIVING":
            return f"Linka {route_short_name} prichádza na zastávku {stop_name}."

        if state == "AT_STOP":
            return f"Linka {route_short_name} stojí na zastávke {stop_name}."

        if state == "DEPARTING":
            return f"Linka {route_short_name} odchádza zo zastávky {stop_name}."

        return None
if state == "MISSED":
    return f"Linka {route_short_name} prešla zastávku {stop_name} bez zastavenia."
