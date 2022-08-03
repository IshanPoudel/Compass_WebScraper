''' Given the starting url , it grabs all the house_card and their respective links.'''

import re
import time
import logging
import csv
from bs4 import BeautifulSoup

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
import traceback
from random import randint
import  config
from main import get_details_from_each_house_link

# later , add it from the sql file.

db = mysql.connector.connect(host="localhost" ,
    user = config.user,
    passwd=config.password ,
    database="REAL_ESTATE_INFORMATION"
    )

mycursor  = db.cursor()


def get_values_for_each_house_and_store():


    mycursor.execute("SELECT link , houseID FROM house_link WHERE DataScraped = false")
    link_and_id = mycursor.fetchall()



    for link , id in link_and_id:



        query = "INSERT INTO house_agent(house_id , street_address , state_address , agent_name , AGENCY , trec ) VALUES (%s , %s , %s , %s , %s , %s)"

        time.sleep(randint(5, 20))
        details = get_details_from_each_house_link(link)

        try:
            #check if no error
            if details[0] != 'ERROR 404 EMPTY':
                # store into database
                mycursor.execute(query, (int(id), str(details[0]), str(details[1]), str(details[2]), str(details[3]), str(details[4])))
                db.commit()

                #update the DataScraped column on house_link
                Q = "UPDATE house_link SET DataScraped = true WHERE houseID=" + str(id)
                mycursor.execute(Q)
                db.commit()

                #print message
                print(details[0] + " " + details[2])
        except:
            print(traceback.format_exc())
            print("Could not update")


        # update to the database
        time.sleep(20)


get_values_for_each_house_and_store()