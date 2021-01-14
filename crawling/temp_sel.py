from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

chromedriver = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get('https://portal.hanyang.ac.kr/index_pre.html?v=20200408')


##log_in
user_name = ''
password = ''
first_id = '/html/body/div[1]/p'
email_id = '//*[@id="userId"]'
password_id = '//*[@id="password"]'
login_button = '//*[@id="hyinContents"]/div[1]/form/div/fieldset/p[3]/a'

first_tag =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, first_id)))
first_tag.click()

email_tag = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, email_id)))
password_tag = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, password_id)))
login_button_tag = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, login_button)))

email_tag.clear()
email_tag.send_keys(user_name)
password_tag.clear()
password_tag.send_keys(password)
login_button_tag.click()


##lecture menu
room_button = '//*[@id="btn_suupHome"]'
my_lecture_room =  WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, room_button)))
my_lecture_room.click()

time.sleep(2)

lecture_buttons = '//td[@class="a-center"]'
lectures = driver.find_elements_by_css_selector('#btn_goSuupHome')


print('강의 갯수 : ', len(lectures))


##each lecture
for lecture in lectures :
    lecture.click()
    time.sleep(10)
    
    driver.switch_to_window(driver.window_handles[1])
    first_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="books-and-tools-link"]/a')) 
        )

    first_button.click()
    time.sleep(6)
    
#     second_button = WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div.bb-offcanvas-panel.bb-offcanvas-right.peek.hide-in-background.panel-has-focus.active.cc_38250_1 > div > div > div > div > div > div > div > bb-partner-user-provisioner > div > div > ng-transclude > div:nth-child(4) > div > div > div:nth-child(2) > div > a > div > bb-ltipc-item > div > div.details > div')) 
#         )
    second_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[5]/div/div/div/div/div/div/div/bb-partner-user-provisioner/div/div/ng-transclude/div[4]/div/div/div[2]/div/a')) 
    )
    second_button.click()
    time.sleep(3)
    
    
    driver.switch_to_window(driver.window_handles[1])
    check_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '/html/body')) 
        #listContainer_row\:0
#         /html/body/div[2]/div[2]/div/div/div[4]/form/div[2]/div[1]/div/table/tbody/tr[1]
        )

#     print("a:",len(check_list))
    print(check_list[0].text)
    
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    time.sleep(3)
    break
time.sleep(3)
driver.quit()




# loop, count = True, 0

# while loop and count < 30:
#     try:
#         element = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#cbox_module > div.u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_favorite > div.u_cbox_paginate > a')) # 2020.10.06 태그 변경 (a -> button)
#         )

#         more_button = driver.find_element_by_css_selector('#cbox_module > div.u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_favorite > div.u_cbox_paginate > a') # 2020.10.06 태그 변경 (a -> button)
#         webdriver.ActionChains(driver).click(more_button).perform()
#         count += 1
#         time.sleep(2)
#     except TimeoutException:
#         loop = False


# comment_box = driver.find_element_by_css_selector('#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul')
# comment_list = comment_box.find_elements_by_tag_name('li')

# for num, comment_item in enumerate(comment_list):
#     try : 
#         print ("[" + str(num + 1) + "]", comment_item.find_element_by_class_name('u_cbox_contents').text)
#     except :
#         continue

# driver.quit()