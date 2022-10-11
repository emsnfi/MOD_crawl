

import os
import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# import xlsxwriter
import pandas as pd
# from retrying import retry
import datetime
import xlwt
import wmi
from selenium.common.exceptions import NoSuchElementException
import time

def buildDriver():

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--auto-open-devtools-for-tabs")

    options.add_argument('--no-sandbox')
    options.page_load_strategy = "eager"

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    return browser

# obtain the folder 
# return dataframe
def folderCollect(browser,first):
    
    if os.path.exists('input'):

        headcol = []
        dirs = os.listdir('input')
        alltable = []
        for file in dirs:

            path = os.getcwd() + "/input/"+ file
            path = path.replace("\\", "/")
            browser.get(path)
            platform = bios_version(browser)
            if first: 
                headcol = thead(browser)
                first = False
            alltable.extend(tbody(browser,platform))

        df = pd.DataFrame(alltable,columns=headcol)
        
        return df
    else:
        os.mkdir('input')
    
    

def thead(browser):
    thead = []
    for i in range(1,9):
        xpath = '//*[@id="summary-table"]/thead/tr/th['+ str(i) + ']'
        thead.append(browser.find_element(By.XPATH,xpath).text)

    temp = thead
    
    temp.insert(4,str(thead[4]))
    temp.insert(7,str(thead[6]))
    temp.insert(8,str(thead[8]))
    temp.insert(0,"Platform")
    return temp

def tbody(browser,platform):
    tbody = []
    row = 1
    while True:

        try:
            xpath = '//*[@id="summary-table"]/tbody/tr['+ str(row) + ']'
            rowlist = browser.find_element(By.XPATH,xpath).text.split('\n')
            
            if len(rowlist) != 11:
                rowlist.insert(8,"-")
            
            rowlist.insert(0,platform)
            tbody.append(rowlist)
            row +=1
        except NoSuchElementException:  
            pass
            break

    return tbody

def bios_version(browser):

    try:
        platform = browser.find_element(By.XPATH,'/html/body/table[1]/tbody/tr[3]/td[2]').text
    
    except NoSuchElementException:  #spelling error making this code not work as expected
        platform = browser.find_element(By.XPATH,'//*[@id="spr-content"]/div/div/table/tbody/tr[3]/td[3]').text
        pass
    
    return platform
    
def exportExcel(df):
    localtime = time.localtime()
    result = time.strftime("%Y-%m-%d%I:%M:%S%p", localtime)
    writer = pd.ExcelWriter("./output/output.xlsx") 
    df.to_excel(writer, sheet_name='demo', index=False, na_rep='NaN')

    col = list(df.columns)
    for index,column in enumerate(col):
        column_width = len(column)
        col_idx = index
        writer.sheets['demo'].set_column(col_idx, col_idx, column_width+5)
    writer.sheets['demo'].autofilter(0,0,0,len(col)-1)

    writer.save()
    os.system("start EXCEL.EXE output.xlsx")

if __name__ == '__main__':
    
    start_time = datetime.datetime.now()
    browser = buildDriver()
    first = True
    df = folderCollect(browser,first)
    exportExcel(df)
    end_time = datetime.datetime.now()
    print("Time:",end_time - start_time)
