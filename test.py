import sys
from typing import List, Optional
from bs4.element import Tag
from dataclasses import dataclass
from numpy import array
import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QUrl, pyqtSignal, QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEnginePage # Load JS (Act like client)
import requests
from bs4 import BeautifulSoup
from secret_url import url
import re
from pandas import DataFrame

class Client(QWebEnginePage):
    toHtmlFinished = pyqtSignal()

    def __init__(self, url):
        self.app=QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()

    def store_html(self, html):
        self.html = html
        self.toHtmlFinished.emit()

    def get_html(self):
        self.toHtml(self.store_html)
        loop = QEventLoop()
        self.toHtmlFinished.connect(loop.quit)
        loop.exec_()
        return self.html

    def scraps_to_txt(self):
        # I really don't know what the w+ was, but wb turns it into binary mode, whatever that is.
        # I changed it because I was getting an encoding error
        with open(r"Scraped_Page.txt", "wb") as file_object:
            for contents in self.html:
                # When writing the contents, I use the encode method with the utf8 argument
                # because it cried about the unicode characters if I didn't have this.
                # Even with it though, it was still broken until I changed w+ to wb 2 lines up.
                file_object.write(contents.encode('utf8'))

@dataclass
class Product:
    vendor: str
    name: str
    weight: str
    thc: str
    cbd: str
    price: str
    
def is_heading_row(row: Tag) -> bool:
    style = row.attrs.get('style')
    return style is not None and 'background-color' in style

def as_product(row: Tag) -> Optional[Product]:
    if is_heading_row(row):
        return None 

    return Product(
    
        vendor = row.select_one('td.ninja_column_0').text,
    
        name   = row.select_one('td.ninja_column_1').text,
    
        weight = row.select_one('td.ninja_column_2').text,
    
        thc    = row.select_one('td.ninja_column_3').text,
    
        cbd    = row.select_one('td.ninja_column_4').text,
    
        price  = row.select_one('td.ninja_column_5').text
    )

class ParseAndPort:
    
    #ninja_column_0 = vendor = ninja_clmn_nm_vendor
    #ninja_column_1 = strain (name) = ninja_clmn_nm_strain
    #ninja_column_2 = WT (weight/mass/quantity) = ninja_clmn_nm_wt
    #ninja_column_3 = THC (percentage) = ninja_clmn_nm_thc
    #ninja_column_4 = CBD (percentage) = ninja_clmn_nm_cbd
    #ninja_column_5 = Price ($) = ninja_clmn_nm_price
    #ninja_column_6 = Terps (what the fuck is a terp?) = ninja_clmn_nm_allterpsblank = all_terps
    #ninja_column_7 = Category (flower? vape? extract? we want vape) = ninja_clmn_nm_category
    #ninja_column_8 = Type (LLR Cart is an example) = ninja_clmn_nm_type
    #ninja_column_9 = Dominance (no fucking clue) = ninja_clmn_nm_dominance
    #ninja_column_10 = Bisabolol (terpene header, percentage) = ninja_clmn_nm_bisabolol = terpene_header
    #ninja_column_11 = Caryophyllene (terpene header, percentage) = ninja_clmn_nm_caryophyllene = terpene_header
    #ninja_column_12 = Humulene (terpene header, percentage) = ninja_clmn_nm_humulene = terpene_header
    #ninja_column_13 = Limonene (terpene header, percentage) = ninja_clmn_nm_limonene = terpene_header
    #ninja_column_14 = Linalool (terpene header, percentage) = ninja_clmn_nm_linalool = terpene_header
    #ninja_column_15 = Myrcene (terpene header, percentage) = ninja_clmn_nm_myrcene = terpene_header
    #ninja_column_16 = Pinene (terpene header, percentage) = ninja_clmn_nm_pinene = terpene_header
    #ninja_column_17 = Terpinolene (terpene header, percentage) = ninja_clmn_nm_terpinolene = terpene_header
    
    """
    This class is responsible for parsing the File_object that was retrieved with PyQt5.
    The file is parsed using the parse_contents() method. Data is then fed into the classes
    li_variables which is then used via class scope in the port_to_dataframe() method. 
    """
    def __init__(self, arg_soup):
        """
        Let the class contain all the lists for re-usablity factor.
        """

    def get_products(self) -> List[Product]:
        rows = soup.select('#footable_7821 > tbody > tr')

        optional_products: List[Optional[Product]] = [as_product(row) for row in rows]

        products: List[Product] = [product for product in optional_products if product is not None]

        return products

secret_url = url
client_response=Client(secret_url)
source=client_response.get_html()
client_response.scraps_to_txt()
File_object = open(r"Scraped_Page.txt")
soup = BeautifulSoup(File_object, "lxml")

data_set = ParseAndPort(soup)

products = data_set.get_products()

if not products:
    print('No products found')

for product in data_set.get_products():
    print(product)

data_set.get_products()
df = DataFrame(products)
df.to_csv('THCcsv.csv')
print(df)

#### headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
#### requested_doc = requests.get(url, headers=headers)
#### 
#### print(f"""\n----STATUS CODE: {requested_doc.status_code}\n""")
#### 
#### soup = BeautifulSoup(requested_doc.text, "lxml") 
#### print(f"""\n----STATUS CODE: {soup.prettify()}\n""")
#### 
#### Main_Target_Container = soup.find_all('a')
#### print(f"MAIN TARGET CONTAINER: {Main_Target_Container}")
#### 
#### print("Done.")