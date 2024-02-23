import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

def initialize_driver():
    """WebDriver 초기화 함수"""
    return wd.Chrome()

def navigate_to_player_records(driver):
    """선수 기록 페이지로 이동하는 함수"""
    target = 'https://portal.kleague.com/user/loginById.do?portalGuest=rstNE9zxjdkUC9kbUA08XQ=='
    driver.get(target)
    driver.execute_script("javascript:moveMainFrame('0011');")
    driver.execute_script("javascript:moveMainFrame('0194');")
    driver.execute_script("javascript:moveMainFrame('0208');")

def extract_table_header(table):
    """테이블 헤더 추출 함수"""
    thead = table.find_element(By.TAG_NAME, "thead")
    return thead.text.strip('시도 성공 성공%').strip('\n')

def merge_column_names(header_text):
    """칼럼 이름 결합 함수"""
    column_names = header_text.split(' ')
    merged_columns = []
    for col in column_names:
        keyword = f'{col}시도 {col}성공 {col}성공%'
        if col in ['드리블', '패스', '전방패스', '후방패스', '횡패스', '공격진영패스', '수비진영패스', '중앙진영패스', '롱패스', '중거리패스', '단거리패스', '크로스', '지상경합', '공중경합', '태클']:
            col = keyword
        merged_columns.append(col)
    return merged_columns

def select_options(driver, selector, options_count):
    """옵션 선택 함수"""
    option_elements = driver.find_elements(By.CSS_SELECTOR, selector)
    option_keys = [option.text for option in option_elements[1:1+options_count]]
    for key in option_keys:
        option_element = driver.find_element(By.CSS_SELECTOR, selector)
        option_element.send_keys(key)
        time.sleep(1)

def scrape_match_data(driver, Match_Data, column_names, year, team, league):
    """경기 데이터 스크랩 함수"""
    match_option = '#selectGameId'
    match_opt = driver.find_element(By.CSS_SELECTOR, match_option)
    match_options = driver.find_elements(By.CSS_SELECTOR, '#selectGameId.select-control > option')
    matches_select = Select(match_opt)
    search_button = '#btnSearch'
    click_button = driver.find_element(By.CSS_SELECTOR, search_button)
    match_keys = [option.text for option in match_options[1:]]
    for match in match_keys:
        round_match = match.replace(' ', '').split('/')
        match_opt.send_keys(match)
        time.sleep(3)  
        click_button.click()
        time.sleep(3)
        datas = []
        table = driver.find_element(By.CSS_SELECTOR, '#playerDataTable')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        if len(table_rows) == 3:
            print('미진행 경기')
            continue
        else:
            for table_row in table_rows[2:]:
                row_data = table_row.text.split(' ')
                if len(row_data) != len(column_names):
                    modified_name = "".join(row_data[1:3])
                    row_data[1:3] = [modified_name]
                datas.append(row_data)
            df = pd.DataFrame(data=datas, columns=column_names)
            add_year = [str(year)] * len(df)
            add_team = [str(team)] * len(df)
            add_round = [round_match[0]] * len(df)
            add_match = [round_match[1]] * len(df)
            df.insert(0, '시즌(년도)', add_year)
            df.insert(1, '소속', team)
            df.insert(2, '라운드', add_round)
            df.insert(3, '상대팀', add_match)
            Match_Data = pd.concat([Match_Data, df])
    return Match_Data

def main():
    driver = initialize_driver()
    navigate_to_player_records(driver)
    table = driver.find_element(By.CSS_SELECTOR, '#playerDataTable')
    header_text = extract_table_header(table)
    column_names = merge_column_names(header_text)
    Match_Data = pd.DataFrame(columns=column_names)
    
    year_selector = '#selectYear.select-control'
    league_selector = '#selectMeetSeq.select-control'
    team_selector = '#selectTeamId.select-control'
    
    year_options_count = 0
    league_options_count = 0
    team_options_count = None  # This will be determined dynamically
    
    select_options(driver, year_selector, year_options_count)
    select_options(driver, league_selector, league_options_count)
    
    year_options = driver.find_elements(By.CSS_SELECTOR, '#selectYear.select-control > option')
    year_keys = [option.text for option in year_options[1:1+year_options_count]]
    league_options = driver.find_elements(By.CSS_SELECTOR, '#selectMeetSeq.select-control > option')
    league_keys = [option.text for option in league_options[1:1+league_options_count]]
    
    for year in year_keys:
        for league in league_keys:
            select_options(driver, team_selector, team_options_count)
            team_options = driver.find_elements(By.CSS_SELECTOR, '#selectTeamId.select-control > option')
            team_options_count = len(team_options) - 1
            team_keys = [option.text for option in team_options[1:]]
            for team in team_keys:
                Match_Data = scrape_match_data(driver, Match_Data, column_names, year, team, league)
    
    driver.quit()

if __name__ == "__main__":
    main()
