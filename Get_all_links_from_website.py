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

from main import get_details_from_each_house_link
import json
import config

db = mysql.connector.connect(host="localhost" ,
    user = config.user,
    passwd=config.password ,
    database="REAL_ESTATE_INFORMATION"
    )

mycursor  = db.cursor()


def parse_links(html):
    links = []

    try:
        soup = BeautifulSoup(html , 'html.parser')
        house_tags = soup.find_all( "div" , {"data-tn":"uc-listingPhotoCard"} )
        links=[]
        for tags in house_tags:

            json_tag = tags.find("script" , {"type" : "application/ld+json" })
            json_tag = json_tag.get_text()



            details_json = json.loads(json_tag)

            links.append(details_json['url'])
            # #from details_json grab the link
            # link = details_json['url']

        return links
    except:
        print(traceback.format_exc())
        # return a empty list
        return links



def update_to_db(house_link):

    if house_link is None:
        print(url + "did not work")

    else:
        for house in house_link:
            # check if it is already in the database.
            # you have an incoming stream of houses , once you reach a house that has already been read previously you stop
            try:
                query = "SELECT link FROM house_link WHERE link = " + " '" + house + "'"
                mycursor.execute(query)
                check_if_present = mycursor.fetchall()

                if not check_if_present:
                    mycursor.execute("INSERT INTO house_link ( link ) VALUES (%s )",
                                     (house,))
                    db.commit()
                    print("Inserted into database")

                if check_if_present:
                    print("Up to Date")
                    print(house + "already in the table")
                    quit()
            except:
                print(traceback.format_exc())
                print("Could not add " + house + "to house_link_table" )


def get_all_links():





    try:



        chrome_options = Options()  # Instantiate an options class for the selenium webdriver
        # chrome_options.add_argument("--headless")  # So that a chrome window does not pop up
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(10)

        #later , add it from the sql file.
        url_list = config.url_list

        for url in url_list:
            time.sleep(10)

            print("Getting links from : " + url)
            driver.get(url)
            time.sleep(20)

            driver.implicitly_wait(10)
            html_text = driver.page_source

            XPATH_TUPLE_FOR_HOUSE_CARDS = (By.XPATH, "/html/body/main/div/div[1]/div[2]/div[1]/div[1]/div")
            driver.implicitly_wait(20)
            data = driver.find_element(*XPATH_TUPLE_FOR_HOUSE_CARDS)
            html_for_house_cards = data.get_attribute('innerHTML')

            get_all_links = parse_links(html_for_house_cards)

            update_to_db(get_all_links)

        driver.close()
    except:
        print(traceback.format_exc())






get_all_links()