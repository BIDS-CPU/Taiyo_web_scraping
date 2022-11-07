# -*- coding: utf-8 -*-
"""Scrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R5NempxHjQfh48EgoyKM4ZLbSs6jHphI
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt


def webscraping():
  baseurl='https://opentender.eu/'
  page=requests.get(baseurl)
  if page.status_code!=200:
    raise Exception('Failed to load page {}'.format(page))
  soup=BeautifulSoup(page.content,'html.parser')


  links=soup.find_all('a')
  country_link=[]
  country_name=[]
  for i in links[6:39]:
    country_link.append(baseurl+i.get('href'))
    country_name.append(i.text)

    count_of_tenders= soup.find_all('div')[21:54]
    tenders = []

    for i in count_of_tenders:
        tenders.append(i.text)
    
    reg = re.compile(r'\d+.?\d+')
    total_tenders = []

    for i in tenders:
        if 'Million' in i:
            mo = reg.findall(i)
            number = float(mo[0]) * 1000000
            total_tenders.append(number)
        else:
            total_tenders.append(i)
        
  df=pd.DataFrame({'Country':country_name,'Number of tenders':total_tenders,'links':country_link,})
  df.to_csv('scrapper.csv', index= False)



a=webscraping()
a

df1=pd.read_csv('scrapper.csv')

df1.dtypes

df1['Number of tenders']=df1['Number of tenders'].str.replace(',','')

df1['Number of tenders']=df1['Number of tenders'].astype(float)

df1

plt.figure(figsize=(15,12))
plt.barh(df1['Country'],df1['Number of tenders'])
plt.xticks(rotation=45)
plt.show()

df1['Number of tenders'].plot(kind='pie',labels=df1['Country'],figsize=(20,12),autopct="%1.2f")

