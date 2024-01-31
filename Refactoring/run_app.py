import selenium
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

def initialize_driver():
    # load selenium webdriver
    driver = wd.Chrome()
    return driver

def login_kleague_portal(driver):
    # go to K-league portal
    target = 'https://portal.kleague.com/user/loginById.do?portalGuest=rstNE9zxjdkUC9kbUA08XQ=='
    driver.get(target)

def move_to_data_center(driver):
    # click data center button
    driver.execute_script("javascript:moveMainFrame('0011');")

def move_to_additional_records(driver):
    # javascript:moveMainFrame('0194'); => click etc button
    driver.execute_script("javascript:moveMainFrame('0194');")

def move_to_player_records(driver):
    # go to player's match data
    driver.execute_script("javascript:moveMainFrame('0208');")

def extract_table_data(driver):
    # extract table data in page
    table = driver.find_element(By.CSS_SELECTOR, '#playerDataTable')
    thead = table.find_element(By.TAG_NAME, "thead")
    tbody = table.find_element(By.TAG_NAME, "tbody")

def remake_thead(thead):
    # replace thead(remaking thead line)
    thead_1 = thead.text.strip('시도 성공 성공%').strip('\n')
    thead_1 = thead_1.replace('유효 슈팅', '유효슈팅').replace('내 슈팅', '내슈팅').replace('외 슈팅', '외슈팅') \
                      .replace('방 패스', '방패스').replace('진영 패스', '진영패스').replace('경합 지상', '지상경합') \
                      .replace('경합 공중', '공중경합')
    
    # combine columns attempt, success, success percent sector
    col = thead_1.split(' ')
    column_name = []
    
    for cl in col:
        keyword = f'{cl}시도 {cl}성공 {cl}성공%'
        if cl in ['드리블', '패스', '전방패스', 
                  '후방패스', '횡패스', '공격진영패스', 
                  '수비진영패스', '중앙진영패스', '롱패스', 
                  '중거리패스', '단거리패스', '크로스', 
                  '지상경합', '공중경합', '태클']:
            cl.replace(cl, keyword)
            column_name.append(keyword)
        else:
            column_name.append(cl)

    cls = ' '.join(column_name)
    column_name = cls.split(' ')

    time.sleep(5)

    return column_name

