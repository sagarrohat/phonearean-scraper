
#Author: Rohat Sagar

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

#returns links and names of all brands
def scrap_brands(url):
    urls = list()
    names = list()
    page = urlopen(url) #open url and get its content
    soup = BeautifulSoup(page,'html.parser')
    makers = soup.find_all('a', class_='ahover') # find all <a> tags with class name ahover
    for x in makers:
        urls.append('https://www.phonearena.com'+x.get('href')) #get value of href attribute of <a>
        name = x.find_all('span',class_='alt') # find all <span> with class name alt inside each <a> tag
        for y in name:
            names.append(y.string)
    return urls,names

#returns links and names of all phones of a brand
def scrap_phones(url):
    urls = list()
    names = list()
    i=1
    while True:
        u = url + '/page/'+str(i)
        page = urlopen(u)
        soup = BeautifulSoup(page,'html.parser')
        phones = soup.find_all('a', class_='thumbnail')
    
        if phones.__len__() < 1:
            break
    
        for x in phones:
            urls.append('https://www.phonearena.com'+x.get('href'))
            name = x.find('p',class_='title')
            names.append(name)
        i = i+1
    return urls,names

#returns the specs of a phone
def scrap_specs(url):
    page = urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    div = soup.find('div', class_='user-rating')
    if div is not None:
        specs = dict()
        rating = div.find('div',class_='progress-value')
        
        features = soup.find_all('div',class_='media-header')
        for f in features: 
            heading = (f.find('div',class_='media-left')).find('h3').string
            specs[str(heading).strip()] = str(f.find('span',class_='size-dimensions-container').string).strip()
        specs['rating'] = rating.string.strip()
        return specs
    return None

#Link contains names,number of phones of all brands and link to page of list of mobiles of that brand
makers = 'https://www.phonearena.com/phones/manufacturers'

#Function which will return list of links to brands and their names
makers_url, makers_name = scrap_brands(makers)

for x in range(84,makers_url.__len__()):
    data = pd.DataFrame()
    print(makers_url[x])
    phones_url,phones_names = scrap_phones(makers_url[x])
    for y in phones_url:
        specs = scrap_specs(y)
        if specs is not None:
            index = [0]
            df =  pd.DataFrame(specs,index=index)
            print(df)
            data = data.append(df,sort=False)
    data.to_csv(str(makers_name[x]+'.csv'))