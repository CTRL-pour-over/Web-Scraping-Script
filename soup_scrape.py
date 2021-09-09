import requests
from bs4 import BeautifulSoup
from requests.models import MissingSchema

class Scraper:
    def __init__(self):
        self.requested_doc = ""
        
    def request_html_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        try:
            requested_doc = requests.get(input("ENTER URL:\n>> "), headers=headers)
            self.view_raw_html(requested_doc)
        except MissingSchema:
            print("Invalid URL")    

    def view_raw_html(self, requested_doc):
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
                    print(f"""\n----STATUS CODE: {requested_doc.status_code}\n""")
                elif x == 2:
                    print(f"""\n----HEADERS: {requested_doc.headers}\n""")
                elif x == 3:
                    print(f"""\n----ENCODING: {requested_doc.encoding}\n""")
                elif x == 4:
                    print(f"""\n----TEXT: {requested_doc.text}\n""")
                elif x == 5:
                    print(f"""\n----JSON: {requested_doc.json}\n""")
                elif x == 6:
                    return self.parse_data() 

            except ValueError:
                print("Incorrect Data Type Used. Script requires an integer to be used.")

    def parse_data(self):
        soup = BeautifulSoup(self.requested_doc, 'html.parser')
        print(f"""
                {soup.title}
                {soup.title.name}
                {soup.title.string}
                {soup.title.parent.name}
                {soup.p} 
                {soup.p['class']}
                {soup.a}
                {soup.find_all('a')}
                {soup.find(id="link3")}     
                """)

def run():
    scrape_instance = Scraper()    
    scrape_instance.request_html_page()

run()
