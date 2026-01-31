import requests
import re
import logging
from bs4 import BeautifulSoup
from settings import BERLIN_WOHNEN_USERNAME, BERLIN_WOHNEN_PASSWORD

logger = logging.getLogger("flat-alert")

class Scraper:
    URL_LOGIN = 'https://www.inberlinwohnen.de/login'
    URL_FINDER = 'https://www.inberlinwohnen.de/mein-bereich/wohnungsfinder'
    BASE_URL = 'https://www.inberlinwohnen.de'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'de,en;q=0.9,en-US;q=0.8',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def login(self):
        logger.info("fetching inberlinwohnen.de login page")
        resp_login_page = self.session.get(self.URL_LOGIN, timeout=30)
        token_search = re.search(r'name="csrf-token" content="([^"]+)"', resp_login_page.text)
        if not token_search:
            logger.critical("no CSRF token found on login page.")
            return False
        csrf_token = token_search.group(1)

        payload_login = {
            '_token': csrf_token,
            'email': BERLIN_WOHNEN_USERNAME,
            'password': BERLIN_WOHNEN_PASSWORD,
            'remember': 'on'
        }
        headers_login = self.HEADERS.copy()
        headers_login['Referer'] = self.URL_LOGIN

        logger.info("attempting login")
        resp_post = self.session.post(self.URL_LOGIN, data=payload_login, headers=headers_login, timeout=30)

        if not resp_post.ok or "login" in resp_post.url:
            logger.critical("login failed")
            logger.info(f"status code: {resp_post.status_code}")
            logger.info(f"url: {resp_post.url}")
            return False
        logger.info("login successful")
        return True

    def get_flats(self):
        logger.info("fetching flat list")
        self.session.headers.update({'Referer': 'https://www.inberlinwohnen.de/mein-bereich'})
        resp_finder = self.session.get(self.URL_FINDER, timeout=30)

        soup = BeautifulSoup(resp_finder.text, 'html.parser')
        apartment_divs = soup.find_all('div', id=re.compile(r'^apartment-\d+'))

        logger.info(f"found {len(apartment_divs)} apartments on page.")
        
        flats_data = []
        for div in apartment_divs:
            flat_id = div['id'].replace('apartment-', '')
            data = {'id': flat_id}

            link_elem = None
            for link in div.find_all('a'):
                if "alle details" in link.get_text(strip=True).lower():
                    link_elem = link.get('href')
                    break

            if link_elem:
                data['link'] = link_elem if link_elem.startswith('http') else self.BASE_URL + link_elem
            else:
                data['link'] = self.BASE_URL

            details_list = div.find('dl')
            if details_list:
                dt_elements = details_list.find_all('dt')
                for dt in dt_elements:
                    key = dt.get_text(strip=True).rstrip(':')
                    dd = dt.find_next_sibling('dd')
                    if dd:
                        data[key] = dd.get_text(strip=True)
            
            flats_data.append(data)
            
        return flats_data
