import requests 
from glob import glob 
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime 
from time import sleep 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

def read_amazon_wishlist():
    products = pd.read_csv("trackers/products.csv", sep = ',')
    product_urls = products.url
    currenttime = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    tracker_log = pd.DataFrame()

    for x, url in enumerate(product_urls):
        page = requests.get(url, headers = HEADERS)
        try:
            page.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        #print(page.text)
        soup = BeautifulSoup(page.content, 'lxml')

        #product title 
        title = soup.find(id ='productTitle').get_text().strip()
        print(title)

        #price 
        try:
            wholenumber = soup.find(class_ = 'a-price-whole').get_text().strip()
        except:
            wholenumber = ''
        try:
            fractionnumber = soup.find(class_ = 'a-price-fraction').get_text().strip()
        except:
            fractionnumber = ''

        price = wholenumber + fractionnumber 
        if price == '':
            print("unable to extract price")
            return 
        print(price)

        dataframe = pd.DataFrame({'date': currenttime.replace('h', ':').replace('m', ''), 
                                  'Product Name': title, 
                                  'Current Price': price}, index = [x])
        if float(price) < float(products['buy_below '][x]):
            print('Alert! Buy the product now. ')
            #implement the twilio api here 

        tracker_log = tracker_log.concat(dataframe)
        print("\n" + title + 'appended to tracker log')
        sleep(5)
    
    excel_log = pd.read_excel('product_logs.xlsx', engine='openpyxl')
    updated_df = excel_log.concat(tracker_log, sort = False)
    updated_df.to_excel('product_logs.xlsx', index = False)

    print('end of search')
    
    


read_amazon_wishlist()







