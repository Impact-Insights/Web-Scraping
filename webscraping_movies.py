import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = 'WebScrapingUsingAPIs/top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

'''Finding the required data in the table using "find_all"
tables gets the body of all the tables in the web page 
and the variable rows gets all the rows of the first table'''



#SCRAPING OF REQUIRED INFORMATION

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

#Iterate over the rows to find the required data

for row in rows:
    if count < 50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {
                "Average Rank": col[0].contents[0],
               "Film": col[1].contents[0],
               "Year": col[2].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
            count+=1

    else:
        break
        
print(df)


#STORING THE DATA INTO A DATABASE

df.to_csv(csv_path)

#Connecting to a database

conn = sqlite3.connect(db_name)
df = df.to_sql(table_name,con = conn, if_exists='replace', index=False)
conn.close()

