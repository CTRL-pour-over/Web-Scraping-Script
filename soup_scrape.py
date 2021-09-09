import requests
from bs4 import BeautifulSoup
from requests.models import MissingSchema

class ScrapeManager:
    def request_html_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        try:
            requested_doc = requests.get(input("ENTER URL:\n>> "), headers=headers)
            self.view_raw_html(requested_doc)
        except MissingSchema:
            print("Invalid URL")    

    def view_raw_html(self, arg_requested_doc):
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

                if x == 1:
                    print(f"""\n----STATUS CODE: {arg_requested_doc.status_code}\n""")
                elif x == 2:
                    print(f"""\n----HEADERS: {arg_requested_doc.headers}\n""")
                elif x == 3:
                    print(f"""\n----ENCODING: {arg_requested_doc.encoding}\n""")
                elif x == 4:
                    print(f"""\n----TEXT: {arg_requested_doc.text}\n""")
                elif x == 5:
                    print(f"""\n----JSON: {arg_requested_doc.json}\n""")
                elif x == 6:
                    self.parse_document(arg_requested_doc) 

            except ValueError:
                print("Incorrect Data Type Used. Script requires an integer to be used.")

    def parse_document(self, arg_requested_doc):
        soup = BeautifulSoup(arg_requested_doc.text, "lxml") 
        self.view_soup(soup)
             
    def view_soup(self, arg_soup):
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

                if x == 1:
                    print(f"""\n----STATUS CODE: {arg_requested_doc.status_code}\n""")
                elif x == 2:
                    print(f"""\n----HEADERS: {arg_requested_doc.headers}\n""")
                elif x == 3:
                    print(f"""\n----ENCODING: {arg_requested_doc.encoding}\n""")
                elif x == 4:
                    print(f"""\n----TEXT: {arg_requested_doc.text}\n""")
                elif x == 5:
                    print(f"""\n----JSON: {arg_requested_doc.json}\n""")
                elif x == 6:
                    self.parse_data(arg_requested_doc) 

            except ValueError:
                print("Incorrect Data Type Used. Script requires an integer to be used.")

def run():
    scrape_instance = ScrapeManager()    
    scrape_instance.request_html_page()

run()
