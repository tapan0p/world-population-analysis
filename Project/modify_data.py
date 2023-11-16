from bs4 import BeautifulSoup
import re

with open('population_data.html','r') as file :
    html_data=file.read()


soup=BeautifulSoup(html_data,'html.parser')


def clean_row(row):
    row_str=str(row)
    row_str=row_str.replace(",","")
    row_str=row_str.replace(" ","")
    row_str=row_str.replace("\n","")
    row_str=re.sub(r'<.*?>', ',',row_str)
    row_str=row_str.replace(",,",",")
    row_str=row_str.replace(",,",",")
    row_str=row_str[1:-1]
    row_data=row_str.split(",")
    return row_data



table=[]

ind=0

for row in soup.find_all('tr'):
    if ind==0 :
        ind+=1
        continue
    
    table.append(clean_row(row))
    
    
#print(table)
