import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape(stu_id:str, password:str) -> list:

    # chrome driverの設定
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    service = fs.Service(CHROMEDRIVER)
    driver = webdriver.Chrome(
        options=options,
        # service=ChromeService(ChromeDriverManager().install())
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
    menuList = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[6]/ul/li[3]/ul")
    driver.execute_script("arguments[0].setAttribute('style','display: block;')", menuList)

    # 履修登録確認にアクセス
    myCalendar = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[6]/ul/li[3]/ul/li[1]/a")
    myCalendar.send_keys(Keys.ENTER)

    # 時間割を抽出
    table = []
    for j in range(3, 16, 2):
        for i in range(3, 14, 2):
            coma_xpath = f"/html/body/div/div[2]/table/tbody/tr/td[1]/form/div[2]/div[3]/table/tbody/tr[{j}]/td[{i}]/table/tbody/tr/td"
            coma = driver.find_element(By.XPATH, coma_xpath)
            coma_text = coma.get_attribute("innerHTML")
            pattern = r'<br>(.*?)<br>'
            matches = re.findall(pattern, coma_text, re.DOTALL)
            table.append(matches[0].strip())
    jikanwari = [table[0:6], table[6:12], table[12:18], table[18:24], table[24:30], table[30:36], table[36:42]]

    # chromeを終了
    driver.close()

    return jikanwari
