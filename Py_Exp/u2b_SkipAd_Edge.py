from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import time

driver = webdriver.Edge()
driver.get("https://www.youtube.com")

# 检测并点击“跳过广告”按钮
def skip_ad():
    ret = True
    try:
        skip_button = driver.find_element(By.CLASS_NAME, "ytp-skip-ad-button")  # YouTube 的“跳过广告”按钮的类名
        if skip_button:
            print("找到跳过广告按钮，点击！")
            ActionChains(driver).move_to_element(skip_button).click().perform()            
    except NoSuchElementException:
        pass    
    except NoSuchWindowException:
        driver.quit()
        ret = False
    except Exception as e:
        pass
        print(f"未找到按钮或出现错误: {e}")
    finally:
        print(ret)
        return ret
# 自动循环检测
while skip_ad():    
    time.sleep(0.5)
