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


def parse_html_to_get_address(html):

   soup = BeautifulSoup(html, 'html.parser')
   street_address_tag = soup.find("p" , { "data-tn" : "listing-page-address" } )
   street_address = street_address_tag.get_text()

   city_address_tag = soup.find("span" , { "class" :"summary__StyledAddressSubtitle-e4c4ok-9 leoAGJ"})
   city_address = city_address_tag.get_text()

   return street_address , city_address

def parse_html_to_get_agent_detail(html):

   soup = BeautifulSoup(html, 'html.parser')

   name_tag = soup.find("p" , { "data-tn" : "contactAgentSlat-view-name" } )
   name = name_tag.get_text()

   agency_name_tag = soup.find("p" , { "data-tn" : "contactAgentSlat-view-displayCompany"} )
   agency_name = 'NULL'
   if agency_name_tag is not None:
     agency_name=agency_name_tag.get_text()

   trec_id_tag = soup.find("p" , { "data-tn" : "contactAgentSlat-view-licenseNumber"} )
   trec_id = re.split("#" , trec_id_tag.get_text() , 1)[-1]

   return name , agency_name , trec_id






def get_details_from_each_house_link(url):

   chrome_options = Options()  # Instantiate an options class for the selenium webdriver
   # chrome_options.add_argument("--headless")  # So that a chrome window does not pop up
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
   time.sleep(10)

   blank_list = []
   blank_list.append("ERROR 404 EMPTY")

   # From website get all the tags
   try:

      driver.get(url)
      time.sleep(20)

      driver.implicitly_wait(10)
      html_text = driver.page_source
      # convert based on 'html parser'

      XPATH_TUPLE_FOR_ADDRESS = (By.XPATH , "//*[@id='overview']/main/div[1]/div[1]/div/div")
      driver.implicitly_wait(10)
      data = driver.find_element(*XPATH_TUPLE_FOR_ADDRESS)
      html_for_address = data.get_attribute('innerHTML')
      street_address , city_address = parse_html_to_get_address(html_for_address)

      driver.implicitly_wait(20)


      XPATH_TUPLE_FOR_AGENT = (By.XPATH ,"//*[@id='listingTeam']/ol/li/div/div[1]/div" )
      driver.implicitly_wait(10)
      data_for_agent = driver.find_element(*XPATH_TUPLE_FOR_AGENT)
      html_for_agent = data_for_agent.get_attribute('innerHTML')
      agent_name , agency_name , trec_id = parse_html_to_get_agent_detail(html_for_agent)

      if len(trec_id) == 7:
         trec_id=trec_id.lstrip("0")
         #remove the first zero


      final_list = ( street_address , city_address , agent_name , agency_name , trec_id )
      driver.close()

      return final_list



   except:
      print(traceback.format_exc())
      driver.close()
      return blank_list



