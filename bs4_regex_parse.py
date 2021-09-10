import re
from bs4 import BeautifulSoup
###########################-----TESTING BS4 REGEX-----##################################


Source_Code = open("Scraped_Page.txt", 'r')

#soup = BeautifulSoup(Source_Code, "html.parser")
#td_tags = soup.find_all('td', class_="ninja_column_0")

#print(td_tags)

keyterms = re.compile(r"([A-Z])\w+s", str(Source_Code))
print(keyterms)
