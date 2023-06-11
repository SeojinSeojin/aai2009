from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from bs4 import BeautifulSoup


# 정보를 저장할 리스트
col = ['일시', '초미세먼지', '미세먼지', '오존', '이산화탄소', '일산화탄소', '아황산가스']
data = []

# 브라우저 자동으로 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def get_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://cleanair.seoul.go.kr/airquality/localAvg')
    time.sleep(3)

    # 측정소명
    driver.find_element(By.XPATH, '//*[@id="lGroup"]').click()
    driver.find_element(By.XPATH, '//*[@id="lGroup"]/option[2]').click()
    driver.find_element(By.XPATH, '//*[@id="mGroup"]').click()
    driver.find_element(By.XPATH, '//*[@id="mGroup"]/option[2]').click()
    
    # 측정 단위
    driver.find_element(By.XPATH, '//*[@id="sGroup"]').click()
    driver.find_element(By.XPATH, '//*[@id="sGroup"]/option[1]').click()

    for i in range(1, 13):
        if i in [1, 3, 5, 7, 8, 10, 12]:
            k = 32
        elif i in [2]:
            k = 29
        else:
            k = 31
        for j in range(1, k):
            if i < 10:
                new_i = str(0) + str(i)
            else:
                new_i = i
            if j < 10:
                j = str(0) + str(j)


            # 측정 일
            day = driver.find_element(By.XPATH, '//*[@id="searchDate"]')
            day.click()
            day.clear()
            day.send_keys(f'2022-{new_i}-{j}')

            # 측정 시
            driver.find_element(By.XPATH, '//*[@id="searchTime"]').click()
            driver.find_element(By.XPATH, '//*[@id="searchTime"]/option[1]').click()

            # 검색
            driver.find_element(By.XPATH, '//*[@id="search"]').click()
            time.sleep(5)

            # 정보 가져오기
            table = driver.find_element(By.XPATH, '//*[@id="localAvg-table"]')
            tbody = table.find_element(By.TAG_NAME, 'tbody')


            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            
            for value in rows:
                date = value.find_elements(By.TAG_NAME, 'td')[0].text.strip()
                pos = value.find_elements(By.TAG_NAME, 'td')[1].text.strip()
                if pos == '도심권':
                    try:
                        cho = value.find_elements(By.TAG_NAME, 'td')[2].text
                        mi = value.find_elements(By.TAG_NAME, 'td')[3].text
                        O3 = value.find_elements(By.TAG_NAME, 'td')[4].text
                        NO2 = value.find_elements(By.TAG_NAME, 'td')[5].text
                        CO = value.find_elements(By.TAG_NAME, 'td')[6].text
                        SO2 = value.find_elements(By.TAG_NAME, 'td')[7].text
                    except Exception as e:
                        print(e)

                    data.append([date, cho, mi, O3, NO2, CO, SO2])
                
    with open('13.csv', 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(col)
        writer.writerows(data)
    

    driver.close()

get_data()
