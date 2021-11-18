import requests
from multiprocessing import Process
import time
import requests
from requests.structures import CaseInsensitiveDict
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os




def watcher(query_data):
    video_id = query_data['video_id']
    user_id = query_data['user_id']
    user_xs = query_data['user_xs']
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    driver.get("https://www.facebook.com")
    print(driver.title)
    driver.add_cookie({'name': 'c_user', 'value': user_id})
    driver.add_cookie({'name': 'xs', 'value': user_xs})
    driver.refresh()
    video_url = f'https://www.facebook.com/watch/live/?ref=watch_permalink&v={video_id}'
    driver.get(video_url)
    if 'checkpoint' in driver.current_url:
        try:
            data = {'error':'Account_blocked','worker':"WORKER_NAME"}
            requests.post("SERVER_URL",json=data)
        except:
            pass
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="presentation"]')))
    time.sleep(10)
    x = driver.find_elements(By.CSS_SELECTOR,'div[role="presentation"]')
    for i in x:
        try:
            i.click()
        except:
            pass



from flask import Flask,request
app = Flask(__name__)

@app.route('/',methods = ["POST","GET"])
def webhook():
    return "OK"
    
    
    
@app.route('/ffb/view',methods = ["POST","GET"])
def api():
    try:
        if request.json != None:
            query_data = []
            query_data.append(request.json)
            task = Process(target=watcher,args = (query_data,))
            task.start()
            return "ok"
        else:
            return "OK"
    except:
        return 'nt'
    
    
@app.route('/wb')
def ma():
    return 'hello'

if __name__ == '__main__':
    app.run()
