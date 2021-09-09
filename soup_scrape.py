import requests
from bs4 import BeautifulSoup
from requests.models import MissingSchema

class ScrapeManager:
    def __init__(self):
        requested_doc = ''

    def request_html_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        try:
            self.requested_doc = requests.get(input("ENTER URL:\n>> "), headers=headers)
            self.view_raw_html()
        except MissingSchema:
            print("Invalid URL")    

    def view_raw_html(self):
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
                    print(f"""\n----STATUS CODE: {self.requested_doc.status_code}\n""")
                elif x == 2:
                    print(f"""\n----HEADERS: {self.requested_doc.headers}\n""")
                elif x == 3:
                    print(f"""\n----ENCODING: {self.requested_doc.encoding}\n""")
                elif x == 4:
                    print(f"""\n----TEXT: {self.requested_doc.text}\n""")
                elif x == 5:
                    print(f"""\n----JSON: {self.requested_doc.json}\n""")
                elif x == 6:
                    return self.parse_document() 
                    
            
            except ValueError:
                print("Incorrect Data Type Used. Script requires an integer to be used.")

    def parse_document(self):
        print("PARSETEST")
        soup = BeautifulSoup(self.requested_doc.text, "lxml") 
        print(soup)
 
def run():
    scrape_instance = ScrapeManager()    
    scrape_instance.request_html_page()

run()
