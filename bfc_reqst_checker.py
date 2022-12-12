from selenium import webdriver
from selenium.webdriver.common.by import By
from win10toast_click import ToastNotifier
import chromedriver_autoinstaller
import time


toast = ToastNotifier()
driver = vars()
global sn
sn = vars()
global chkedLst
chkedLst = []


def main():
    global driver, sn
    try:
        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')

        ##크롬드라이브 위치 주의
        #driver = webdriver.Chrome(r'C:/Users/blues/dev_files/chromedriver.exe', options=options)
        driver = webdriver.Chrome(options=options)

        ##로그인 URL 설정
        driver.get('url')
        driver.implicitly_wait(10)

        driver.find_element(By.NAME, 'mng_id').send_keys('id')
        driver.find_element(By.NAME, 'password').send_keys('pw')
        driver.find_element(By.XPATH, "//input[@class='btn_login']").click()
        driver.implicitly_wait(10)
        time.sleep(3)

        print(f"[{time.strftime('%x %X')}][DEBUG] success login.")

        cnt = 1
        while True:
            driver.refresh()
            driver.implicitly_wait(10)
            time.sleep(3)

            reqTbl = driver.find_element(By.ID, 'ncomGridLst_AX_tbody')
            reqLst = reqTbl.find_elements(By.TAG_NAME, 'tr')
            print(f"[{time.strftime('%x %X')}][DEBUG] cycle {cnt}")
            for tr in reqLst:
                tdLst = tr.find_elements(By.TAG_NAME, 'td')

                gbn = vars()
                stt = vars()
                tit = vars()
                usr = vars()

                for i in range(len(tdLst)):
                    if i == 0:
                        sn = tdLst[i].text
                    elif i == 2:
                        gbn = tdLst[i].text
                    elif i == 3:
                        stt = tdLst[i].text
                    elif i == 4:
                        tit = tdLst[i].text
                    elif i == 5:
                        usr = tdLst[i].text
                if stt == '요청':
                    print(f"[{time.strftime('%x %X')}][INFO] : [{sn}][{stt}] {gbn} - {tit}")
                    if sn not in chkedLst:
                        showToast(gbn, stt, tit, usr)
                    else:
                        print(f"Checked No. {sn}")
                print(f'[{time.strftime("%x %X")}][DEBUG] : Checked No. {chkedLst}')
            time.sleep(180)
            cnt += 1
    except:
        print(f"[{time.strftime('%x %X')}][ERROR] exception.")
        driver.quit()
        main()


def addChk():
    global sn
    chkedLst.append(sn)

def showToast(gbn: str, stt: str, tit: str, usr: str):
    toast.show_toast(
        f"[{stt}] {gbn}",
        f"{tit}",
        duration=10,
        threaded=False,
        callback_on_click=addChk,
    )


if __name__ == '__main__':
    main()
