import re
import time
import logging
import csv
import traceback
import concurrent.futures
from bs4 import BeautifulSoup


import threading
from threading import Lock

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import mysql.connector
from random import randint
import xlrd
import pandas as pd
import config




db = mysql.connector.connect(host="localhost",
                             user=config.user,
                             passwd=config.password,
                             db='real_estate_information'

                             )

mycursor = db.cursor()


# read csv file

data = pd.read_excel(r'trecfile.xlsx')
print("I finished reading the excel file")
data.columns = ['TREC_ID' ,'NAME' ,'PHONE' , 'EMAIL' , 'STREET' , 'CITY' , 'STATE' , 'ZIP' ]
df = data.iloc[ :  , :]

count =0
for  row in df.itertuples():
    try:
        # print(row[0])
        # print(row[1])
        # print(row[2])
        # print(row[3])
        trec = str(row[1]).strip()
        address= str(row[5]) + " " + str(row[6]) + " " + str(row[7]) + " " + str(row[8])
        # print(str(row[4]) + " " + str(row[5]) + " " + str(row[6]) + " " + str(row[7]))
        query = "INSERT INTO agent_record(trec_id , name , phone_number , email  , address ) VALUES (%s , %s , %s , %s , %s)  "
        mycursor.execute(query , (trec , str(row[2]) , str(row[3]) , str(row[4]) , address ))

        print("Added agent " + str(row[1])+"'s record.")
        db.commit()
    except:
        print("Error")
        print(traceback.format_exc())



print("total" + str(count))


# for values in df:
#     if not values:
#         values = " "
#
# trec = str(df[0])
# name = str(df[1])
# phone = str(df[2])
# email = str(df[3])
# address = str(df[4]) + " " + str(df[5]) + " " + str(df[6])+ " " + str(df[7])
#
    # print(row['TREC_ID'])
    # print(row['NAME'])
    # print(row['PHONE'])
    # print(row['EMAIL'])
    # print(row['STREET'] + " " + row['CITY'] + " " + row['STATE'] + " " + row['ZIP'])