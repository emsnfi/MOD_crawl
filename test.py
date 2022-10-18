from concurrent.futures import thread
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
from thread import*
import re
import tkinter.font as font

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
def folderCollect(browser,first,checkBox):
    
    if os.path.exists('input'):

        headcol = []
        dirs = os.listdir('input')
        alltable = []
        fileUrl = []
        for file in dirs:
            # the file will be one column
            path = os.getcwd() + "/input/"+ file
            path = path.replace("\\", "/")

            browser.get(path) # main thread
            platform = bios_version(browser) # contain bios & version
            if first:  
                # t1 = threading.Thread(target = thead,args=(browser,))
                # t1.start()
                headcol = thead(browser)
                first = False
            temp = tbody(browser,platform,file,checkBox)
            length = len(temp)
            tempurl = [file] * length
            fileUrl.extend(tempurl)

            alltable.extend(temp) # content

            # alltable.extend(tbody(browser,platform,file,checkBox))

        df = pd.DataFrame(alltable,columns=headcol)
        urlcol = ["url"]
        fileUrl = pd.DataFrame(fileUrl,columns=urlcol)
        df["File Name"] = fileUrl["url"].apply(lambda x: make_hyperlink(x))
        
       
        return df
    else:
        os.mkdir('input')

def make_hyperlink(value):
    # url = "https://custom.url/{}"
    url = os.getcwd() + "/input/{}"
    url = url.replace("\\", "/")
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)
  
# thead thread
def theadThread():
    the = MyThread(thead)
    the.start()
    theadresult = the.get_result() # get tbody result
    return theadresult


def thead(browser):
    thead = []
    
    i = 1
    while True:
        
        try:
        
           if i not in [2,3]: # delete start time & duration
                xpath = '//*[@id="summary-table"]/thead/tr/th['+ str(i) + ']'
                thead.append(browser.find_element(By.XPATH,xpath).text)
            
            
        except NoSuchElementException:  
            pass
            break
        i += 1

    temp = thead
    temp.insert(1,"File Name") # file name
    temp.insert(2,"Platform") # BIOS 
    temp.insert(3,"Version") # version
    
    temp.insert(6,"Energy Change"+" % " +"of Battery")
    temp.insert(7,"Change Rate mW")
    
    temp[5] = "Energy Change mWh"
    temp[9] = "SW Drip %"
    temp.insert(10,"HW Drip %")
    
    temp[4] = "State"
    temp[8] = "Change Rate"
    temp[11] = "% Capacity Remaining at Start"
    
    return temp


# tbody thread
def tbodyThread():
    tbo = MyThread(tbody)
    tbo.start()
    tbodyresult = tbo.get_result() # tbody result
    return tbodyresult


def tbody(browser,platform,fileName,checkBox):
    tbody = []
    row = 1
    while True:

        try:
            xpath = '//*[@id="summary-table"]/tbody/tr['+ str(row) + ']'
            rowlist = browser.find_element(By.XPATH,xpath).text.split('\n')
            # when checkbox is 1, only dispay sleep state data
            if checkBox ==1 and rowlist[3] != "Sleep":
                row +=1
                continue
                
            print("Sleep",rowlist)
            # 	% LOW POWER STATE TIME is divided into sw drip, hw drip
            if len(rowlist) < 11:
                rowlist.insert(9,"-")

            rowlist.insert(1,fileName) # add file name
            rowlist.insert(2,platform[0]) # add bios 
            rowlist.insert(3,platform[1]) # add version
            
            if "Drain" in rowlist[10] : # only keep drain status CHANGE RATE
                
                filter(rowlist)
                tbody.append(rowlist)

            row +=1
        except NoSuchElementException:  
            pass
            break

    return tbody

def filter(rowlist): 
    

    rowlist.pop(4) # delete start time column data
    rowlist.pop(4) # delete duration column data

    # delete the unit except for the last column 5 6 8 9 
    for i in [5,6,7,9,10]:
        rowlist[i] = re.sub("\D","",rowlist[i])


    return rowlist
    
    


    
def bios_version(browser):

    try: # for win10 /html/body/table[1]/tbody/tr[3]/td[2]
        platform = browser.find_element(By.XPATH,'/html/body/table[1]/tbody/tr[3]/td[2]').text
        bios = platform.split()[0]
        version = platform.split()[2]

    except NoSuchElementException:  #win11 spelling error making this code not work as expected
        platform = browser.find_element(By.XPATH,'//*[@id="spr-content"]/div/div/table/tbody/tr[3]/td[3]/span[1]').text
        bios = platform.split()[0]
        version = platform.split()[2]
        pass
    
    return bios,version


def exportExcel(df):
    # localtime = time.localtime()
    if not os.path.exists('output'):
        os.mkdir('output')


    # result = time.strftime("%Y-%m-%d%I:%M:%S%p", localtime)
    writer = pd.ExcelWriter("./output/output.xlsx") 
    df.to_excel(writer, sheet_name='demo', index=False, na_rep='NaN')
    workbook  = writer.book
    
    # formatAlign = workbook.add_format({'align': 'center'})
    format = workbook.add_format()
    format.set_align('center')
    format.set_align('vcenter')
    
    col = list(df.columns)
    for index,column in enumerate(col):
        column_width = len(column)
        col_idx = index
        if index != 1:
            writer.sheets['demo'].set_column(col_idx, col_idx, column_width+5,format)
        
        else:
            writer.sheets['demo'].set_column(col_idx, col_idx, column_width+5)
        # writer.sheets['demo'].set_column('index:index',5, format)
    writer.sheets['demo'].autofilter(0,0,0,len(col)-1)
    
    
    writer.save()
    os.system("start EXCEL.EXE ./output/output.xlsx")


def createWindow():
    
    
    global docTypes
    global stop_threads
    global startTrans
    startTrans = True
    stop_threads = False
    
    instructions = '  Use this tool to report test logs.\n\n     1. Put the HTML log files in the input folder.\n\n     2. Click Start.\n\n  Wait a moment 😊 \n\n  Then, the report spreadsheet will be \n\n  automatically opened and saved in the\n\n  output folder.'
    root = Tk()
    # btn = Button(root, text='Start', command=changeText)  
    def Transform(checkBox):
        start_time = datetime.datetime.now()
        browser = buildDriver()
        first = True
        df = folderCollect(browser,first,checkBox)
        exportExcel(df)
        end_time = datetime.datetime.now()
        changeText()
        
        print("Time:",end_time - start_time)
        startTrans = True

    def changeText(): # change button content
        if(button['text']=='Start'):
            button['text']='Stop'
        else:
            button['text']='Start'
    
    
    def Transthreading():

        # Two condition:
        # when start -> start the thread
        # when stop -> stop (terminate) the thread

         checkBox = check.get()
         if(button['text']=='Start'):
            button['text']='Stop'
           
            button['bg'] = "#f7e4ee"
            t1 = MyThread(Transform,args=(checkBox,))
            # t1 = threading.Thread(target=) 
            
            t1.start()
         else:
            print(threading.enumerate()[1]) #
            threading.enumerate()[1].raise_exception()
            
            # terminate transform thread 
            # turn stop button to start
            button['bg'] = "#e4f7ea"
            button['text']='Start'

    # def show():
    #     label.config( text = var1.get() )
    
    # def getValue():
        # label.config( text = var1.get() )

    root.geometry('400x520+250+50')
    root.title('Power Report')
    # t = threading.Thread(target=Transform)
    toolLabel = Label(root, justify=LEFT, text='Power Report', font=("Arial",15), height=3, width=200)
    toolLabel.pack()
    T = Label(root, text=instructions, height=15, width=38, bg='white', font=("Arial",12), relief=SUNKEN, bd=4, justify=LEFT)
    T.pack()   
    
    myFont = font.Font(size=11)
    # show warning message when click stop button
    # root.messagebox.showwarning(title="Warning message", message="Do you really want to stop processing")
    check = IntVar() # checked is 1, non checked is 0
    checkBtn = Checkbutton(root, text="Display only Sleep State", variable=check, height = 2)
    # checkBtn.grid(row=1, sticky=W) # cannot get it 
    checkBtn["font"] = myFont
    checkBtn.pack(padx = 10,pady=10)
    # button = Button( root , text = "click Me" , command = show ).pack()
    # label = Label( root , text = " " )
    # label.pack()
    # button = Button(root, text = 'Start', command= lambda:[changeText(),Transthreading()], width = 8, height = 3, fg = 'black' )
    button = Button(root, text = 'Start', command=lambda: Transthreading(), width = 8, height = 2, fg = 'Black' ,bg="#e4f7ea")
    button["font"] = myFont
    button.pack(padx = 10, pady = 10)

    # button = Button(root, text = 'see value', command= Transthreading, width = 8, height = 3, fg = 'black' )
    # button.info
    # if start:
    #     button = Button(root, text = 'Start', command=threading1(start) , width = 8, height = 3, fg = 'black' )
    
    # els button = Button(root, text = 'Stop', command=threading1(start) , width = 8, height = 3, fg = 'black' )
    
   
    
    
    root.mainloop()






if __name__ == '__main__':
    
    createWindow()
   
