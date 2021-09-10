from typing import Callable, Dict
import requests
from bs4 import BeautifulSoup
from requests.models import MissingSchema, Response
from enum import Enum

class ScrapeManager:
    def __init__(self):
        self.response: Response = None

    def request_html_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        try:
            self.response = requests.get(input("ENTER URL:\n>> "), headers=headers)
            self.view_raw_html()
        except MissingSchema:
            print("Invalid URL")    

    def view_raw_html(self):
        mapping: Dict[UserSelection, Callable[[], None]] = {
            UserSelection.STATUS_CODE: lambda: print(f"""\n----STATUS CODE: {self.response.status_code}\n"""),
            UserSelection.HEADERS:     lambda: print(f"""\n----HEADERS: {self.response.headers}\n"""),
            UserSelection.ENCODING:    lambda: print(f"""\n----ENCODING: {self.response.encoding}\n"""),
            UserSelection.TEXT:        lambda: print(f"""\n----TEXT: {self.response.text}\n"""),
            UserSelection.JSON:        lambda: print(f"""\n----JSON: {self.response.json}\n"""),
            UserSelection.PARSE_DATA:  lambda: self.parse_document()
        }

        mapping[get_user_selection()]()

    def parse_document(self):
        soup = BeautifulSoup(self.response.text, "lxml") 
        print(soup.prettify())
 

class UserSelection(Enum):
    STATUS_CODE = 1
    HEADERS = 2
    ENCODING = 3
    TEXT = 4
    JSON = 5
    PARSE_DATA = 6

def get_user_selection() -> UserSelection:
    while True:
        try:
            x = int(input("""
                        TYPE AN INT TO SHOW DATA:
                        1) STATUS CODE
                        2) HEADERS
                        3) ENCODING
                        4) TEXT
                        5) JSON
                        6) PARSE DATA
                        \n>> """))

            if 1 <= x <= 6:
                return UserSelection(x)

        except ValueError:
            print("Incorrect Data Type Used. Script Requires Int.")

def run():
    scrape_instance = ScrapeManager()    
    scrape_instance.request_html_page()

run()