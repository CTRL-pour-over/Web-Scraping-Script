from secret_url import url
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
requested_doc = requests.get(url, headers=headers)

print(f"""\n----STATUS CODE: {requested_doc.status_code}\n""")

soup = BeautifulSoup(requested_doc.text, "lxml") 
print(f"""\n----STATUS CODE: {soup.prettify()}\n""")

print("Done.")