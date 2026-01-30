import re
from urllib.parse import quote
from rich.markup import escape

import maps


class Flat:
    def __init__(self, data):
        self.link = data.get('link', '')
        self.address = data.get('Adresse', '')
        self.rooms = self._parse_german_float(data.get('Zimmeranzahl', '0'))
        self.size = self._parse_german_float(data.get('Wohnfläche', '0'))
        self.cold_rent = self._parse_german_float(data.get('Kaltmiete', '0'))
        self.utilities = self._parse_german_float(data.get('Nebenkosten', '0'))
        self.total_rent = self._parse_german_float(data.get('Gesamtmiete', '0'))
        self.available_from = data.get('Bezugsfertig ab', '')
        self.published_on = data.get('Eingestellt am', '')
        self.wbs = data.get('WBS', '')
        self.floor = data.get('Etage', '')
        self.bathrooms = data.get('Badezimmer', '')
        self.year_built = data.get('Baujahr', '')
        self.heating = data.get('Heizung', '')
        self.energy_carrier = data.get('Hauptenergieträger', '')
        self.energy_value = data.get('Energieverbrauchskennwert', '')
        self.energy_certificate = data.get('Energieausweis', '')
        self.raw_data = data
        self.id = self.link  # we could use data.get('id', None) but link is easier to debug
        self.gmaps = maps.Maps()
        self._connectivity = None
        self.address_link_gmaps = f"https://www.google.com/maps/search/?api=1&query={quote(self.address)}"

    def __str__(self):
        # URL encode the link to ensure it doesn't contain characters that break markup
        # We preserve characters that are standard in URLs but encode problematic ones like brackets and spaces
        safe_chars = ":/?#@!$&'()*+,;=%-"
        escaped_link = quote(self.link, safe=safe_chars)
        return f"[link={escaped_link}]{escape(self.address)}[/link]"

    def _parse_german_float(self, text):
        if not text:
            return 0.0
        clean_text = re.sub(r'[^\d,.]', '', text)
        clean_text = clean_text.replace('.', '').replace(',', '.')
        try:
            return float(clean_text)
        except ValueError:
            return 0.0

    @property
    def sqm_price(self):
        if self.size > 0:
            return self.total_rent / self.size
        return 0.0

    @property
    def connectivity(self):
        if not self._connectivity:
            self._connectivity = self.gmaps.calculate_score(self.address)
        return self._connectivity

    @property
    def display_address(self):
        if ',' in self.address:
            parts = self.address.split(',', 1)
            street_part = parts[0].strip()
            city_part = parts[1].replace(',', '').strip()
            return f"{street_part}\n{city_part}"
        else:
            return self.address
