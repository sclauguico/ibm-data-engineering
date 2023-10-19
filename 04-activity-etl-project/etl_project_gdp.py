# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime 
from bs4 import BeautifulSoup

log_file = "log_file.txt"
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_name = 'Movies.db'
table_name = 'Countries_by_GDP'
csv_path = 'Counties_by_GDP.csv'
attribute_list = ['Country', "GDP_USD_millions"]

conn = sqlite3.connect('GDP.db')

def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    df = pd.DataFrame(columns=attribute_list)

    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    

    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
    return df

# My Solution:
def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''

    df['GDP_USD_millions'] = df['GDP_USD_millions'].str.replace('[^\d.]', '', regex=True).astype(float)
    df['GDP_USD_millions'] = (df['GDP_USD_millions'] / 1000).round(2)
    df = df.rename(columns={'GDP_USD_millions': 'GDP_USD_billions'})

    return df

# Exercise Recommmended Solution:
# def transform(df):
#     GDP_list = df["GDP_USD_millions"].tolist()
#     GDP_list = [float("".join(x.split(','))) for x in GDP_list]
#     GDP_list = [np.round(x/1000,2) for x in GDP_list]
#     df["GDP_USD_millions"] = GDP_list
#     df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
#     return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists = 'append', index =False)

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthcar_model-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 
''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''


# Log the initialization of the ETL process 
log_progress("ETL Job Started") 

# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract(url, attribute_list) 
print("Extracted Data") 
print(extracted_data) 

# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 

# Log the beginning of the load csv process 
log_progress("Load to csv phase Started") 
loaded_csv_data = load_to_csv(transformed_data, csv_path) 
print("Loaded CSV Data") 
print(loaded_csv_data) 

# Log the beginning of the load to database process 
log_progress("Load to database phase Started") 
loaded_db_data = load_to_db(transformed_data, conn, table_name) 

# Log the beginning of the running of query process 
log_progress("Run Query Started") 
query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
read_query_data = run_query(query_statement, conn)

conn.close()