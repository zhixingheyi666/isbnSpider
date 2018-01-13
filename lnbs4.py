#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .fc.conn_SQL import mkcon
from .fc.LOG_sf import logger
from urllib.request import urlopen
from bs4 import BeautifulSoup


cursor, mconn = mkcon()
cursor.execute('''use fortest''')
tturl = 'http://www.pythonscraping.com/pages/page3.html'
tthtml = urlopen(tturl)
ttbsObj = BeautifulSoup(tthtml,'html.parser')
zzurl = 'http://www.pythonscraping.com/pages/warandpeace.html'
zzhtml = urlopen(zzurl)
zzbsObj = BeautifulSoup(zzhtml,'html.parser')

driver1t=webdriver.Firefox()
driver1t.get(tturl)
driver2z=webdriver.Firefox()
driver2z.get(zzurl)

def startFox(url = 'http://www.baidu.com', keY = 'wd'):
    driver=webdriver.Firefox()
    driver.get(url)
    try:
        elem = driver.find_element_by_name(keY)
        elem.send_keys('selenuim')
        elem.send_keys(Keys.RETURN)
    except:
        logger.exception('Info:\n')
#    finally:
#        driver.close()
#        driver.quit()
