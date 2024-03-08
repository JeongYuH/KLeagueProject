import selenium
import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import re

# Load Chrome Driver

def call_web_driver(drive_path):
    '''
        Before launch driver, you should set driver path for chrome_driver!
    '''
    driver = wd.Chrome()
    # K-League Data portal page(If you use other root, solve frame problem.)
    target = 'https://portal.kleague.com/user/loginById.do?portalGuest=rstNE9zxjdkUC9kbUA08XQ=='
    driver.get(target)

    driver.execute_script("javascript:moveMainFrame('0011');")              # Press data center button

    driver.execute_script("javascript:moveMainFrame('0194');")              # javascript:moveMainFrame('0194'); => Click etc button

    driver.execute_script("javascript:moveMainFrame('0208');")              # Match data per player link
    return driver

def table_setting(driver):
    time.sleep(1)
    table = driver.find_element(By.CSS_SELECTOR, '#playerDataTable')
    
    # thead
    thead = table.find_element(By.TAG_NAME, "thead")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    # table is consist two lines, that disturb make our thead.
    thead_1 =  thead.text.strip('시도 성공 성공%').strip('\n')
    # Definition of dictionary for replacing words.
    
    replacement_dict = {
        '유효 슈팅': '유효슈팅',
        '내 슈팅': '내슈팅',
        '외 슈팅': '외슈팅',
        '방 패스': '방패스',
        '진영 패스': '진영패스',
        '경합 지상': '지상경합',
        '경합 공중': '공중경합'
    }
    replacement_list = ['드리블', '패스', '크로스', '경합', '태클']

    # Replacing words(for removing Space)
    for original, replacement in replacement_dict.items():
        thead_1 = thead_1.replace(original, replacement)
    # Concat words from specific items to Attempt, Success, Percentage of success
    col = thead_1.split(' ')
    test = col.copy()
    for word in replacement_list:
        for idx, i in enumerate(test):
            if word in i and i != '키패스':
                a = f'{i}시도 {i}성공 {i}성공%'
                test[idx] = a
    test = ' '.join(test)
    col = test.split(' ')
    return col

def call_year(driver, year=None):
    year_option = '#selectYear.select-control'  # CSS 선택자
    year_opt = driver.find_element(By.CSS_SELECTOR, year_option)
    year_options = driver.find_elements(By.CSS_SELECTOR, '#selectYear.select-control > option')
    teams_select = Select(year_opt)
    year_li = year_opt.text
    year_list = year_li.split('\n')
    y_keys = [ option.text for option in year_options[1:1+5] ]  # You can use 2024 - 2020
    if year is not None:
        year_opt.send_keys( year )
        time.sleep(1)
        return driver
    else:
        for y in y_keys:
            print(y)
            year_opt = driver.find_element(By.CSS_SELECTOR, year_option)
            year_opt.send_keys( y )   
            time.sleep(1)
            return driver


if __name__ == "__main__":
    driver = call_web_driver("C:\\Users\\bewis\\OneDrive\\문서\\python module\\chrome-win64\\chrome.exe")
    table_setting(driver)
    call_year(driver)   # You can add year only [2024:2020] EX) call_year(driver, 2020)
    driver.quit()