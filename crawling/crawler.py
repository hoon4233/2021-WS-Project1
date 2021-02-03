import requests
import json
import os
import sys
import colorama
import urllib3
urllib3.disable_warnings()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

WEB_DRIVER = 'C:\chromedriver.exe'
#WEB_DRIVER = '/usr/local/bin/chromedriver'  
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('--disable-gpu')
option.add_argument('lang=ko_KR')
driver = webdriver.Chrome(WEB_DRIVER, chrome_options=option)


class HYUBlackboard:
    def __init__(self, cookie):
        self.BbRouter = cookie
        self.url = 'https://learn.hanyang.ac.kr'
        self.session = requests.Session()


    def get_user_key(self):
        url = self.url + '/ultra/course'
        cookies = {'BbRouter': self.BbRouter}
        rep = self.session.get(url, cookies=cookies, verify=False)
        idx = rep.text.index('"id":') + 6
        self.user_key = ''
        while rep.text[idx] != '"' and rep.text[idx] != '?':
            self.user_key += rep.text[idx]
            idx += 1
        

    def get_courses(self):
        url = self.url + \
            f'/learn/api/v1/users/{self.user_key}/memberships?expand=course.effectiveAvailability,course.permissions,courseRole&includeCount=true&limit=10000'
        cookies = {'BbRouter': self.BbRouter}
        rep = self.session.get(url, cookies=cookies, verify=False)
        self.courses = []
        for course in json.loads(rep.text)['results']:
            course = course['course']
            dic = {}
            dic['name'] = course['name']
            dic['id'] = course['id']
            dic['courseId'] = course['courseId']
            dic['term'] = course['term']['name'] if 'term' in course else 'None'
            self.courses.append(dic)

    def print_courses(self):
        for course in self.courses:
            print(course, sep=' ')

    def get_attendance(self):
        global driver

        result = dict()

        for course in self.courses :
            result[course['name']] = []

            url = f"https://learn.hanyang.ac.kr/webapps/blackboard/execute/blti/launchPlacement?blti_placement_id=_17_1&course_id={course['id']}&from_ultra=true"

            parent_window = driver.current_window_handle 
            driver.execute_script("window.open('" +url+ "')") 

            all_windows = driver.window_handles
            child_window = [window for window in all_windows if window != parent_window][0]
            driver.switch_to.window(child_window) 
            
            try :
                driver.find_element_by_id('listContainer_showAllButton').click()
            except :
                pass

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            try :
                tbody = soup.find('tbody',{'id':'listContainer_databody'})
            except :
                # print("출석 정보가 없습니다.")
                result[course['name']].append("출석 정보가 없습니다.")
                continue

            try :
                contents = tbody.findAll('span',{'class':'table-data-cell-value'})
            except :
                # print("출석 정보가 없습니다.")
                result[course['name']].append("출석 정보가 없습니다.")
                continue
            
            for idx in range(0,len(contents),7):
                tmp = dict()
                tmp['week'] = contents[idx].text
                tmp['content_name'] = contents[idx+1].text
                tmp['learning_time'] = contents[idx+2].text
                tmp['accreditation_time'] = contents[idx+3].text
                tmp['content_time'] = contents[idx+4].text
                tmp['progress_rate'] = contents[idx+5].text
                tmp['attendance_state'] = contents[idx+6].text

                result[course['name']].append(tmp)


            driver.close() 
            driver.switch_to.window(parent_window)  

        return result



def get_BbRouter(id, pw):
    global driver
    driver.get('https://learn.hanyang.ac.kr/ultra/institution-page')
    driver.implicitly_wait(10)

    driver.find_element_by_id('entry-login-custom').send_keys(Keys.ENTER)
    driver.find_element_by_id('uid').send_keys(id)
    driver.find_element_by_id('upw').send_keys(pw)
    driver.find_element_by_id('login_btn').click()
    driver.switch_to.alert.accept()
    for cookie in driver.get_cookies():
        if cookie['name'] == 'BbRouter':
            return cookie['value']
    print(f'{colorama.Fore.RED}[-] login failed')
    assert(False)

def main():
    colorama.init(autoreset=True)

    print(f'{colorama.Fore.LIGHTBLACK_EX}Blackboard crawler start !')
    id = input('ID: ')
    pw = input('PASSWORD: ')
    
    cookie = get_BbRouter(id, pw)

    blackboard = HYUBlackboard(cookie)
    blackboard.get_user_key()
    blackboard.get_courses()
    result = blackboard.get_attendance()

    print("IN main, result :",result)

    return result
    


if __name__ == '__main__':
    main()

