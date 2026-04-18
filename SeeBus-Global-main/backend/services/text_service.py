class TextService:

    def generate_text_message(self, state, route_short_name, stop_name):
        """
        Vytvorí textové hlásenie pre nepočujúcich.
        """

        if state == "ARRIVING":
            return f"Linka {route_short_name} sa blíži k zastávke {stop_name}."

        if state == "AT_STOP":
            return f"Linka {route_short_name} je na zastávke {stop_name}."

        if state == "DEPARTING":
            return f"Linka {route_short_name} odchádza zo zastávky {stop_name}."

        if state == "MISSED":
            return f"Linka {route_short_name} minula zastávku {stop_name}."

        return None
