import logging

import googlemaps
from datetime import datetime, timedelta, time as dt_time
from settings import GMAPS_API_KEY

logger = logging.getLogger("flat-alert")

class Maps:
    DESTINATIONS = {
        "Hbf": "Berlin Hauptbahnhof",
        "Friedrichstr": "Friedrichstraße, Berlin",
        "Kotti": "Kottbusser Tor, Berlin",
        "Warschauer": "Warschauer Straße, Berlin",
        "Ostkreuz": "Ostkreuz, Berlin",
        "Nollendorf": "Nollendorfplatz, Berlin",
        "Zoo": "Zoologischer Garten, Berlin",
        "Kudamm": "Kurfürstendamm, Berlin",
        "Gesundbrunnen": "Gesundbrunnen, Berlin",
        "Hermannplatz": "Hermannplatz, Berlin"
    }

    def __init__(self):
        self.gmaps = googlemaps.Client(key=GMAPS_API_KEY)

    def _get_next_weekday(self, date, weekday):
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return date + timedelta(days_ahead)

    def _calculate_transfers(self, steps):
        transit_count = sum(1 for step in steps if step['travel_mode'] == 'TRANSIT')
        return max(0, transit_count - 1)

    def calculate_score(self, origin_address):
        now = datetime.now()
        # Next Monday 8:00 AM
        next_monday = self._get_next_weekday(now, 0)
        morning_departure = datetime.combine(next_monday.date(), dt_time(8, 0))
        # Next Sunday 2:00 AM
        next_sunday = self._get_next_weekday(now, 6)
        night_departure = datetime.combine(next_sunday.date(), dt_time(2, 0))

        total_morning_minutes = 0
        total_morning_transfers = 0
        total_night_minutes = 0
        total_night_transfers = 0
        dest_count = 0

        for key, dest_address in self.DESTINATIONS.items():
            # Morning: Flat -> Center
            routes_morning = self.gmaps.directions(
                origin=origin_address,
                destination=dest_address,
                mode="transit",
                departure_time=morning_departure
            )

            # Night: Center -> Flat
            routes_night = self.gmaps.directions(
                origin=dest_address,
                destination=origin_address,
                mode="transit",
                departure_time=night_departure
            )

            if routes_morning:
                leg = routes_morning[0]['legs'][0]
                total_morning_minutes += leg['duration']['value'] / 60
                total_morning_transfers += self._calculate_transfers(leg['steps'])

            if routes_night:
                leg = routes_night[0]['legs'][0]
                total_night_minutes += leg['duration']['value'] / 60
                total_night_transfers += self._calculate_transfers(leg['steps'])

            dest_count += 1

        avg_m_time = total_morning_minutes / dest_count if dest_count else 0
        avg_m_trans = total_morning_transfers / dest_count if dest_count else 0
        avg_n_time = total_night_minutes / dest_count if dest_count else 0
        avg_n_trans = total_night_transfers / dest_count if dest_count else 0

        return {
            'morning_time': avg_m_time,
            'morning_transfers': avg_m_trans,
            'night_time': avg_n_time,
            'night_transfers': avg_n_trans
        }
