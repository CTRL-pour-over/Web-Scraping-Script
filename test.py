import sys
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
        File_object = open(r"Scraped_Page.txt", "wb") #I really don't know what the w+ was, but wb turns it into binary mode, whatever that is. I changed it because I was getting an encoding error
        for contents in self.html:
            File_object.write(contents.encode('utf8')) #When writing the contents, I use the encode method with the utf8 argument because it cried about the unicode characters if I didn't have this. Even with it though, it was still broken until I changed w+ to wb 2 lines up.
        File_object.close()

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
        self.li_Vendor = []
        self.li_Strain = []
        self.li_Straintype = []
        self.li_Weight = []
        self.li_THC_Contents = [] 
        self.li_CBD_Contents = [] 
        self.li_Type = [] 
        self.li_Price = []
        self.li_THCwt = []
        self.li_PpTHC = []

    def parse_contents(self) -> list:
        col = soup.find_all(class_="ninja_column_1")
        for contents in col:
            string = contents.find_next_sibling(class_="ninja_column_7")
            try:
                category = re.search('>(.+?)</td>', str(string)).group(1)
            except AttributeError:
                category = re.search('>(.+?)</td>', str(string))
            if category == "vape": # filtering only by vapes rn, possibilities are flower, vape, extract, edible, tincture, topical, Merchandise, and None(though i think that just means no match was found)
        #note, below code may potentially need altered if anything other than vape is used. all labeled columns and their presumed contents are modeled based on the vape table. others are untested.
                priceelem = string.find_previous_sibling(class_="ninja_column_5")
                try:
                    price = re.search('span>(.+?)</td>', str(priceelem)).group(1)
                except:
                    price = re.search('span>(.+?)</td>', str(priceelem))
                #print(price)
                if price != "$" and price != "":
                    vendorelem = string.find_previous_sibling(class_="ninja_column_0")
                    vendor = re.search('>(.+?)</td>', str(vendorelem)).group(1)
                    strainelem = string.find_previous_sibling(class_="ninja_column_1")
                    #strain = re.search('>(.+?)<img alt>', str(strainelem)).group(1) # returning extra bullshit rn
                    strain = strainelem.get_text().strip() #using a text strip instead of regex because it was being annoying. could probably do this for the rest of them, but too little too late i guess
                    try: #searches for the strain type by assuming that the first match for alt='contents' in the ninja_column_1 element will be part of the img tag for the strain type icon
                        straintype = re.search('alt=\"(.+?)\"', str(strainelem)).group(1)
                    except AttributeError:
                        straintype = re.search('alt=\"(.+?)\"', str(strainelem))
                    wtelem = string.find_previous_sibling(class_="ninja_column_2")
                    try:
                        wt = re.search('>(.+?)</td>', str(wtelem)).group(1)
                    except:
                        wt = re.search('>(.+?)</td>', str(wtelem))
                    #print(wt)
                    if wt != None:
                        thcelem = string.find_previous_sibling(class_="ninja_column_3")
                        #print(thcelem)
                        thc = re.search('>(.+?)</td>', str(thcelem)).group(1)
                        if thc != "0.00%" and thc != None:
                            #print(thc)
                            cbdelem = string.find_previous_sibling(class_="ninja_column_4")
                            cbd = re.search('>(.+?)</td>', str(cbdelem)).group(1)
                            typeelem = string.find_next_sibling(class_="ninja_column_8")
                            type = re.search('>(.+?)</td>', str(typeelem)).group(1)
                            price2 = price.strip("$") #strips out $ symbol so price can be used in calculations
                            thcpercent = thc.strip("%") # strips out % symbol so thc percentage can be used in calculations
                            convwt = re.sub("[^0-9.]", "", wt) # strips everything out of weight except for numbers and periods
                            #print(convwt)
                            match = re.match('\d+mg', str(wt), re.IGNORECASE)#checks to see if it's in milligrams
                            if match is None: #runs this if it's not in milligrams to convert to milligrams (making the assumption it's in grams instead)
                                convwt = float(convwt)*1000
                            #print(convwt)
                            #print(thcpercent)
                            thcwt = (float(convwt) * (float(thcpercent)/100)) #the amount of substance that's actual thc, achieved by multiplying the total weight/mass by the percentage of thc/100 SOME OF THE SHIT IS IN GRAMS LIKE 1G
                            #print(strain + " " + wt + " " + thc + " " + str(price2) + " " + str(thcwt) + " " + str(thcpercent) + " " + str(convwt))
                            #print(thcwt)
                            ppthc = (float(price2)/float(thcwt)) #the price of 1mg of thc per substance. like golf, lower = better
                            #print(vendor + " " + type + " " + strain + " " + wt + " " + thc + " " + cbd + " " + price + " " + str(thcpercent) + " " + str(convwt) + " " + str(thcwt) + " " + str(ppthc))
                            #print(vendor + " " + type + " " + strain + " " + wt + " " + thc + " " + cbd + " " + price)
                            self.li_Vendor.append(vendor)
                            self.li_Strain.append(strain)
                            self.li_Straintype.append(straintype)
                            self.li_Weight.append(wt)
                            self.li_THC_Contents.append(thc)
                            self.li_Type.append(type)
                            self.li_Price.append(price)
                            self.li_THCwt.append(thcwt)
                            self.li_PpTHC.append(ppthc)


    def port_to_dataframe(self):
        dict = {
        "----Vendor----": self.li_Vendor,
        "----Strain----": self.li_Strain,
        "----Straintype----": self.li_Straintype,
        "----Weight----": self.li_Weight,
        "----THC Contents----": self.li_THC_Contents,
        "----Type----": self.li_Type,
        "----Price----": self.li_Price,
        "----mg of THC----": self.li_THCwt,
        "----Price Per mg of THC----": self.li_PpTHC
        }
        df = DataFrame(dict)
        df.to_csv("THCcsv.csv")
        print(df)

    def print_attr_length(self):
        print(self.li_Vendor ,len(self.li_Vendor))
        print(self.li_Strain ,len(self.li_Strain))
        print(self.li_Straintype ,len(self.li_Straintype))
        print(self.li_Weight ,len(self.li_Weight))
        print(self.li_THC_Contents ,len(self.li_THC_Contents))
        print(self.li_CBD_Contents ,len(self.li_CBD_Contents))
        print(self.li_Type ,len(self.li_Type))
        print(self.li_Price ,len(self.li_Price))
        print(self.li_THCwt ,len(self.li_THCwt))
        print(self.li_PpTHC ,len(self.li_PpTHC))

secret_url = url
client_response=Client(secret_url)
source=client_response.get_html()
client_response.scraps_to_txt()
File_object = open(r"Scraped_Page.txt")
soup = BeautifulSoup(File_object, "lxml")

data_set = ParseAndPort(soup)
data_set.parse_contents()
data_set.print_attr_length()
data_set.port_to_dataframe()


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