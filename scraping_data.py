#import necessary libraraies
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scraping_data() :
    results=dict()
    url='https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table'
    html=requests.get(url).text
    soup=BeautifulSoup(html,'html.parser')
    #find the first instance of html tag
    tables=soup.find_all('table')
    for index,table in enumerate(tables):
        if ("wikitable sortable notheme plainrowheaders jquery-tablesorter" in str(table)):
               table_index = index
    Tokyo_olympics=pd.DataFrame(columns=["Rank","Noc","Gold","Silver","Bronze","Total"])
    for row in tables[table_index].tbody.find_all("tr") :
        col=row.find_all("td")
        if col!=[]:
            if len(col)==5  :
                Rank=col[0].get_text()
                past_rank = Rank
                Gold=col[1].get_text()
                Silver=col[2].get_text()
                Bronze=col[3].get_text()
                Total =col[4].get_text()
            else :
                Rank= past_rank
                Gold=col[0].get_text()
                Silver=col[1].get_text()
                Bronze=col[2].get_text()
                Total =col[3].get_text()
        col1=row.find_all("th")
        anchor_tag=col1[0].find("a")
        if anchor_tag :
             Noc=anchor_tag.get_text()
             Tokyo_olympics = pd.concat([Tokyo_olympics, pd.DataFrame([{"Rank": Rank, "Noc": Noc, "Gold": Gold, "Silver": Silver, "Bronze": Bronze, "Total": Total}])], ignore_index=True)
    return Tokyo_olympics
print(scraping_data())

