

import os
import json
from bs4 import BeautifulSoup
import requests

# Opening the html file
# HTMLFile = open("./win11logs/sleepstudy-report.html", "r")
  
# Reading the file
# index = HTMLFile.read()
# # print(index)
# # Creating a BeautifulSoup object and specifyin
# # soup = BeautifulSoup(index, 'lxml')
# soup = BeautifulSoup(index, 'html.parser')
# # print(soup.select('script')[1])
# article = str(soup.select('script')[1])
# # results = json.loads(article)
# [x.extract() for x in soup.findAll(['script', 'style'])]
# print(results)
# data = json.loads(soup.find('script', type='application/ld+json').text)
# print(data)

# response = requests.get("./win11logs/sleepstudy-report.html")
# soup = BeautifulSoup(response.text)
# print(soup)

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
            # print(row)
            if len(rowlist) != 11:
                rowlist.insert(8,"-")
            # elem.click()
            rowlist.insert(0,platform)
            tbody.append(rowlist)
            row +=1
        except NoSuchElementException:  #spelling error making this code not work as expected
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
    writer = pd.ExcelWriter("output.xlsx") 
    # workbook  = writer.book
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
'''
# get url seperate
browser.get(url) 

# element = seek(browser,"summary-table")
bios_version = browser.find_element(By.XPATH,'/html/body/table[1]/tbody/tr[3]/td[2]').text
element = browser.find_element(By.XPATH,'//*[@id="summary-table"]/tbody')
# print(element.text.split("\n"))
thead = []
for i in range(1,9):
    xpath = '//*[@id="summary-table"]/thead/tr/th['+ str(i) + ']'
    thead.append(browser.find_element(By.XPATH,xpath).text)
# print(thead)
temp = thead
temp.insert(4,str(thead[4]))
temp.insert(7,str(thead[6]))
temp.insert(8,str(thead[8]))
# write in excel

# tbody get according to the row
tbody = []
for i in range(1,20):
     xpath = '//*[@id="summary-table"]/tbody/tr['+ str(i) + ']'
     rowlist = browser.find_element(By.XPATH,xpath).text.split('\n')
     if len(rowlist) != 11:
          rowlist.insert(8,"-")
     tbody.append(rowlist)
df = pd.DataFrame(tbody,columns=temp)
df.insert(0,'Platform', bios_version)

# tbody get according to the column

tbodycol = []
# for i in range(1,20):
#     for j in range(1,10):
#         xpath = '//*[@id="summary-table"]/tbody/tr['+ str(i) + ']/td[' + str(j) + ']'
#         colist = browser.find_element(By.XPATH,xpath).text.split('\n')
        
# //*[@id="summary-table"]/tbody/tr[1]/td[4]
writer = pd.ExcelWriter("output.xlsx") 
# workbook  = writer.book
df.to_excel(writer, sheet_name='demo', index=False, na_rep='NaN')

col = list(df.columns)
for index,column in enumerate(col):
    column_width = len(column)
    col_idx = index
    writer.sheets['demo'].set_column(col_idx, col_idx, column_width+5)
writer.sheets['demo'].autofilter(0,0,0,len(col)-1)

writer.save()

os.system("start EXCEL.EXE output.xlsx")
# excel_writer.save()

# df.to_excel('output.xlsx')
end_time = datetime.datetime.now()
print("Time:",end_time - start_time)

# while True:
#     try:
#         browser.find_element_by_xpath('//button[text()="Dodaj u korpu"]')
#     except NoSuchElementException:
#         driver.refresh()
#     else:
#         driver.find_element_by_xpath('//button[text()="Dodaj u korpu"]').click()
#         break
'''