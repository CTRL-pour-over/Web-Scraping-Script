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
        user_selection = get_user_selection()

        if user_selection == UserSelection.STATUS_CODE:
            print(f"""\n----STATUS CODE: {self.response.status_code}\n""")
        elif user_selection == UserSelection.HEADERS:
            print(f"""\n----HEADERS: {self.response.headers}\n""")
        elif user_selection == UserSelection.ENCODING:
            print(f"""\n----ENCODING: {self.response.encoding}\n""")
        elif user_selection == UserSelection.TEXT:
            print(f"""\n----TEXT: {self.response.text}\n""")
        elif user_selection == UserSelection.JSON:
            print(f"""\n----JSON: {self.response.json}\n""")
        elif user_selection == UserSelection.PARSE_DATA:
            self.parse_document()

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