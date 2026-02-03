import time
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console

from settings import *
from paths import *
from utils import *
from flat import Flat
from scraper import Scraper
from telegram import Telegram
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True, console=Console(width=110))]
    )
    logging.getLogger("googlemaps").setLevel(logging.WARNING)

logger = logging.getLogger("flat-alert")
setup_logging()


class FlatAlerter:
    def __init__(self):
        self.checked_ids = self.load_checked_ids()
        self.last_response_hash = ""

    def load_checked_ids(self):
        if not os.path.exists(ALREADY_NOTIFIED_FILE):
            return list()
        with open(ALREADY_NOTIFIED_FILE, "r") as f:
            return list(line.strip() for line in f.read().splitlines())

    def save_checked_id(self, flat_id):
        if flat_id not in self.checked_ids:
            self.checked_ids.append(flat_id)
            with open(ALREADY_NOTIFIED_FILE, "a") as f:
                f.write(f"{flat_id}\n")

    def compose_message(self, flat):
        return (
            f"[{flat.display_address}]({flat.address_link_gmaps})\n"
            f"Miete: {flat.total_rent} ({flat.sqm_price:.2f} €/m²)\n"
            f"Fläche: {flat.size}\n"
            f"Zimmer: {flat.rooms}\n"
            f"Baujahr: {flat.year_built}\n"
            f"WBS: {flat.wbs}\n"
            f"Anb. 8Uhr: {flat.connectivity['morning_time']:.1f} min ({flat.connectivity['morning_transfers']:.1f} Umst.)\n"
            f"Anb. 2Uhr: {flat.connectivity['night_time']:.1f} min ({flat.connectivity['night_transfers']:.1f} Umst.)\n"
            f"[Zur Anzeige]({flat.link})"
        )

    def is_flat_meeting_criteria(self, flat):
        if flat.id in self.checked_ids:
            logger.info("\talready checked")
            return False
        elif flat.rooms not in [2.0, 2.5]:
            logger.info("\twrong room number")
            return False
        elif flat.total_rent > 1500:
            logger.info("\ttoo expensive")
            return False
        elif flat.published_on != datetime.now().strftime("%d.%m.%Y"):
            logger.info("\tnot published today")
            return False
        elif flat.connectivity['morning_time'] > 50:
            logger.info("\tbad connectivity")
            return False
        else:
            logger.info("\tflat meeting all criteria")
            return True

    def scan_and_notify(self):
        logger.info("performing flat scan, filter, notify")
        scraper = Scraper()
        if not scraper.login():
            return

        telegram = Telegram()

        flats_data = scraper.get_flats()

        response_hashed = hash_any_object(flats_data)
        if response_hashed == self.last_response_hash:
            logger.info("flats did not change - skipping loop")
            return
        self.last_response_hash = response_hashed

        for number, data in enumerate(flats_data, 1):
            flat = Flat(data)
            logger.info(f"{str(number).rjust(2)}: checking {flat}")

            if self.is_flat_meeting_criteria(flat):
                msg = self.compose_message(flat)
                logger.info("\tsending telegram message")
                telegram.send_message(msg)
            self.save_checked_id(flat.id)
        logger.info("finished flat scan, filter, notify")

if __name__ == "__main__":
    logger.info("starting flat-alert container")
    flat_alerter = FlatAlerter()
    while True:
        try:
            flat_alerter.scan_and_notify()
            logger.info("sleeping for 60 seconds")
            time.sleep(TIME_INTERVALL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.exception("unexpected error")
            time.sleep(1000)
