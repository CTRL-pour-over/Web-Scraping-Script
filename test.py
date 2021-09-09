import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QUrl, pyqtSignal, QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEnginePage # Load JS (Act like client)
import requests
from bs4 import BeautifulSoup
from secret_url import url


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
        File_object = open(r"Scraped_Page.txt", "w+")
        for contents in self.html:
            File_object.write(contents)

secret_url = url
client_response=Client(secret_url)
source=client_response.get_html()
client_response.scraps_to_txt()

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