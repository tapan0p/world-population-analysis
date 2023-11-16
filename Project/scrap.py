import requests
from bs4 import BeautifulSoup


def scrap(url):
    response=requests.get(url)
    if response.status_code==200 :
        #print(response.text)
        soup=BeautifulSoup(response.text,'html.parser')
        #print(soup.prettify())
        with open('population_data.txt','w') as file :
            file.write(str(soup))
    else :
        print("Access failure")



url="https://www.worldometers.info/world-population/population-by-country"

scrap(url)