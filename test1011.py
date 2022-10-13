import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
from selenium.common.exceptions import NoSuchElementException
import time
import tkinter as tk
from tkinter import *
import sys
import threading


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
            browser.get(path) # main thread
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
    # result = time.strftime("%Y-%m-%d%I:%M:%S%p", localtime)
    writer = pd.ExcelWriter("./output/output.xlsx") 
    df.to_excel(writer, sheet_name='demo', index=False, na_rep='NaN')

    col = list(df.columns)
    for index,column in enumerate(col):
        column_width = len(column)
        col_idx = index
        writer.sheets['demo'].set_column(col_idx, col_idx, column_width+5)
    writer.sheets['demo'].autofilter(0,0,0,len(col)-1)

    writer.save()
    os.system("start EXCEL.EXE ./output/output.xlsx")


def createWindow():
    global docType
    instructions = '  Use this tool to compile test logs.\n\n     1. Put the HTML log files in the input folder.\n\n     2. Click OK.\n\n     The script creates a spreadsheet in the\n     output folder.'
    root = Tk()

def Transform():
        start_time = datetime.datetime.now()
        browser = buildDriver()
        first = True
        df = folderCollect(browser,first)
        exportExcel(df)
        end_time = datetime.datetime.now()
        print("Time:",end_time - start_time)
        
    # def exit():
    #     sys.exit("interrupt running") 
"""
root.geometry('400x500+250+50')
root.title('Test Log Compiler')

toolLabel = Label(root, justify=LEFT, text='Test Log Compiler', font=("Arial",12), height=2, width=200)
toolLabel.pack()
T = Label(root, text=instructions, height=14, width=40, bg='white', font=("Arial",9), relief=SUNKEN, bd=4, justify=LEFT)
T.pack()        
buttonOk = Button(root, text = 'Ok', command = Transform , width = 4, height = 2, fg = 'black' )
# buttonStop = Button(root, text = 'stop', command = exit , width = 4, height = 2, fg = 'black' )
buttonOk.pack(padx = 10, pady = 10)
# buttonStop.pack(padx = 5, pady = 20)

root.mainloop()

"""




if __name__ == '__main__':
    
    Transform()
   
