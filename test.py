import requests
from bs4 import BeautifulSoup
import time 
 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

import sqlalchemy as db

engine = db.create_engine('sqlite:///transcripts.sqlite')
metadata = db.MetaData()
transcripts = db.Table(
   'transcripts', 
   metadata, 
   db.Column('id', db.Integer, primary_key = True), 
   db.Column('link', db.String), 
   db.Column('text', db.String),
   db.Column('start', db.String),
   db.Column('end', db.String),
)
metadata.create_all(engine)

# start by defining the options 
options = webdriver.ChromeOptions() 
options.headless = True # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(5)

video = "https://www.youtubetranscript.com/?v=SJNbnVjecf0"

driver.get(video)

conn = engine.connect()
#driver.find_elements(By.CLASS_NAME)
links = driver.find_elements(By.CLASS_NAME, 'youtube-marker')
for element in links:
    text = element.text
    start = element.get_attribute('data-start')
    end = element.get_attribute('data-end')
    my_data=(None,video,text,start,end)
    #print(start)
    # q="INSERT INTO transcripts values(?,?,?,?,?)"
    ins = transcripts.insert()
    ins = transcripts.insert().values(link=video,text=text, start = start, end=end)
    #conn = engine.connect()
    result = conn.execute(ins)
    conn.commit()

time.sleep(10)