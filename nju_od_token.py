# 获取 OneDrive Cookie, 用于 rclone 挂载
# 2024.1 更新: 现在 OneDrive 只有 100GB, 比较鸡肋

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

driver = webdriver.Remote(
    "http://192.168.1.55:4444/wd/hub", options=webdriver.ChromeOptions()
)
driver.get("https://authserver.nju.edu.cn/")
driver.add_cookie({"name": "CASTGC", "value": "TGT-xxxxxx"})
driver.get("https://ehall.nju.edu.cn/appShow?appId=6322932255269301")


time.sleep(10)
try:
    driver.find_element(By.ID, "idSIButton9").click()
except:
    pass

time.sleep(3)

driver.save_screenshot("test.png")
driver.get(
    "https://njuedu-my.sharepoint.cn/personal/211250000_365_nju_edu_cn/_layouts/15/onedrive.aspx"
)

time.sleep(5)
driver.save_screenshot("test2.png")
print(driver.get_cookies(), file=sys.stderr)

print(
    """
[local]
type = memory

[njuod]
type = webdav
url = https://njuedu-my.sharepoint.cn/personal/211250000_365_nju_edu_cn/Documents/
vendor = sharepoint-ntlm
headers = Cookie,FedAuth="""
    + driver.get_cookie("FedAuth")["value"]
    + ";rtFa="
    + driver.get_cookie("rtFa")["value"]
)

driver.quit()
