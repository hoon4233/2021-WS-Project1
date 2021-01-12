import requests
import json
import os
import sys
import colorama
import urllib3
urllib3.disable_warnings()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from bs4 import BeautifulSoup as bs
import bs4 

WEB_DRIVER = '/usr/local/bin/chromedriver'  

class HYUBlackboard:
    def __init__(self, cookie):
        self.BbRouter = cookie
        self.url = 'https://learn.hanyang.ac.kr'
        self.session = requests.Session()


    def get_user_key(self):
        url = self.url + '/ultra/course'
        cookies = {'BbRouter': self.BbRouter}
        rep = self.session.get(url, cookies=cookies, verify=False)
        # print(rep.text)
        idx = rep.text.index('"id":') + 6
        self.user_key = ''
        while rep.text[idx] != '"' and rep.text[idx] != '?':
            self.user_key += rep.text[idx]
            idx += 1
        print(
            f'{colorama.Fore.GREEN}[+]{colorama.Fore.RESET} user_key: {colorama.Fore.CYAN}{self.user_key}')

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

    def print_present(self):
        # cid = '_39722_1'
        def first():
            cid = '_46942_1'
            url = self.url + \
                f'/learn/api/public/v1/lti/placements?courseId={cid}&type=Application' #_39722_1 => 이거 코스 아이디임. 현재 값은 씨융세2
            cookies = {'BbRouter': self.BbRouter}
            rep = self.session.get(url, cookies=cookies, verify=False)

            # print(json.loads(rep.text)['results'] )
            name = str()
            url = str()

            for button in json.loads(rep.text)['results'] :
                if button['id'] == '_17_1' :
                    name = button['name']
                    url = button['url']
                print(button['url'])
            print("name : ", name, ", url : ",url)
            return url

#여기서부터 문제
        # url = first() + f'?showAll=true&custom_user_id={student_id}&custom_course_id='+'_46942_1'
        url = 'https://learn.hanyang.ac.kr/webapps/bbgs-OnlineAttendance-BB5a998b8c44671/app/atdView?showAll=true&custom_user_id=' + "2016025105" + '&custom_course_id=' + "_46942_1"
        print(url)
        cookies = {'BbRouter': self.BbRouter}
        rep = self.session.get(url, cookies=cookies, verify=False)
        print(rep.text )
        # print(json.loads(rep.text) )



def get_BbRouter(id, pw):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--disable-gpu')
    option.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(WEB_DRIVER, chrome_options=option)
    driver.get('https://learn.hanyang.ac.kr/ultra/institution-page')
    driver.implicitly_wait(10)
    driver.find_element_by_id('entry-login-custom').send_keys(Keys.ENTER)
    driver.find_element_by_id('uid').send_keys(id)
    driver.find_element_by_id('upw').send_keys(pw)
    driver.find_element_by_id('login_btn').click()
    # driver.switch_to.alert.accept()
    for cookie in driver.get_cookies():
        if cookie['name'] == 'BbRouter':
            return cookie['value']
    print(f'{colorama.Fore.RED}[-] login failed')
    assert(False)

def main():
    colorama.init(autoreset=True)

    print(f'{colorama.Fore.LIGHTBLACK_EX}Blackboard Downloader')
    id = input('ID: ')
    pw = input('PASSWORD: ')

    cookie = get_BbRouter(id, pw)

    blackboard = HYUBlackboard(cookie)
    blackboard.get_user_key()
    blackboard.get_courses()
    blackboard.print_courses()
    blackboard.print_present()
    


if __name__ == '__main__':
    main()


# {"id":"_16_1","name":"온라인 출석 콘텐츠 생성","handle":"online-content","type":"Application","url":"https://learn.hanyang.ac.kr/webapps/bbgs-OnlineAttendance-BB5a998b8c44671/app/xinics/importCreate","allowStudents":false,"allowGrading":false,"availability":{"available":"Yes"},"launchInNewWindow":false,"launchLink":"/webapps/blackboard/execute/blti/launchPlacement?blti_placement_id=_16_1&wrapped=true","customParameters":{"course_id":"@X@course.id@X@","user_id":"@X@user.batch_uid@X@"}},

