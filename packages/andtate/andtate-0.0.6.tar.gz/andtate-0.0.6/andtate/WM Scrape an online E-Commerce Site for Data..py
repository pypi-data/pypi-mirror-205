# Only Works on IDLE
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service

s= Service('C:/web driver/chromedriver_win32/chromedriver.exe')
driver =  webdriver.Chrome(service=s)
url="https://www.amazon.in/s?k=books&crid=FW7RDE7ZO0FO&sprefix=%2Caps%2C241&ref=nb_sb_ss_recent_1_0_recent"
driver.get(url)

#List to store details of books
books= []
prices=[]
ratings=[]

content=driver.page_source
soup= BeautifulSoup(content, 'html.parser')
list = soup.find_all('div', attrs={'class':'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right'})

for i in list:
    book = i.find("span",attrs={'class':'a-size-medium a-color-base a-text-normal'})
    print(book.text)
    books.append(book.text)
    price = i.find("span",attrs={'class':'a-price-whole'})
    print(price.text)
    prices.append(price.text)
    rating= i.find("span",attrs={'class':'a-icon-alt'})
    print(rating.text)
    ratings.append(rating.text)
driver.close()

df=pd.DataFrame({'Book Nmae':books, 'Price':prices, 'Rating':ratings})
df.to_csv('Books.csv', index=False, encoding='utf-8')
