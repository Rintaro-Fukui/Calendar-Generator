import os
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape(stu_id:str, password:str):

    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    service = fs.Service(CHROMEDRIVER)

    driver = webdriver.Chrome(
        options=options,
        service=service
        )

    # urlを指定
    url="https://muscat.musashino-u.ac.jp/portal/top.do"
    driver.get(url)

    # 学籍番号を入力
    login = "s" + str(stu_id)
    driver.find_element(By.XPATH,"//*[@id='userId']").send_keys(login)

    # パスワードを入力
    driver.find_element(By.XPATH,"//*[@id='password']").send_keys(password)

    # ログインボタンをクリック
    btn = driver.find_element(By.XPATH,"//*[@id='loginButton']")
    btn.click()

    # メニューの非表示を解除
    menuList = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[6]/ul/li[2]/ul")
    driver.execute_script("arguments[0].setAttribute('style','display: block;')", menuList)

    # my時間割にアクセス
    myCalendar = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[6]/ul/li[2]/ul/li[1]/a")
    myCalendar.send_keys(Keys.ENTER)

    jikanwari = []

    for i in range(1, 5):

        if i != 1:

            # 1学期でない場合は学期を切り替える
            xpath = f"/html/body/div/div[2]/table/tbody/tr/td[1]/form/div[2]/div[2]/div/ul/li[{i}]/a"
            Calendar = driver.find_element(By.XPATH, xpath)
            Calendar.send_keys(Keys.ENTER)

            # 時間割を抽出
            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")
            table = str(bs.find_all("table", class_="detail jikanwari_table"))
            table = re.findall(r"<!-- コマに対応する時間割情報が存在しない場合、縦幅を確保する -->|<a.*?>(.*?)</a>", table)
            jikanwari_ = [table[0:6], table[6:12], table[12:18], table[18:24], table[24:30], table[30:36], table[36:42]]
            jikanwari.append(jikanwari_)

        else:

            # 時間割を抽出
            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")
            table = str(bs.find_all("table", class_="detail jikanwari_table"))
            table = re.findall(r"<!-- コマに対応する時間割情報が存在しない場合、縦幅を確保する -->|<a.*?>(.*?)</a>", table)
            jikanwari_ = [table[0:6], table[6:12], table[12:18], table[18:24], table[24:30], table[30:36], table[36:42]]
            jikanwari.append(jikanwari_)

    driver.close()

    return jikanwari