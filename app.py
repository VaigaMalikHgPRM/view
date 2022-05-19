import requests
from multiprocessing import Process
import time
import requests
from requests.structures import CaseInsensitiveDict
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def watcher(query_data):
    video_id = query_data[0]['video_id']
    user_id = query_data[0]['user_id']
    user_xs = query_data[0]['user_xs']
    driver.get("https://www.facebook.com")
    print(driver.title)
    driver.add_cookie({'name': 'c_user', 'value': user_id})
    driver.add_cookie({'name': 'xs', 'value': user_xs})
    driver.refresh()
    print(driver.title)
    video_url = f'https://www.facebook.com/watch/live/?ref=watch_permalink&v={video_id}'
    driver.get(video_url)
    print(driver.title)
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="presentation"]')))
        time.sleep(10)
        x = driver.find_elements(By.CSS_SELECTOR,'div[role="presentation"]')
        for i in x:
            try:
                i.click()
            except:
                pass
    except:
        pass
    print(driver.title)
    try:
        driver.find_element(By.CSS_SELECTOR,'div[aria-label="Play video"]').click()
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.SPACE)
        except:
            pass
    
def like_post(query_data):
    user_id = query_data[0]['user_id']
    user_xs = query_data[0]['user_xs']
    post_url = query_data[0]['post_url']
    driver.get('https://d.facebook.com')
    driver.add_cookie({'name': 'c_user', 'value': user_id})
    driver.add_cookie({'name': 'xs', 'value': user_xs})
    driver.refresh()
    driver.get(post_url)
    time.sleep(3)
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    x = driver.find_elements_by_css_selector('a[role="button"]')
    for i in x:
        if i.text == 'Like':
            i.click()
    driver.save_screenshot('static/screen.png')

def comment_post(query_data):
    user_id = query_data[0]['user_id']
    user_xs = query_data[0]['user_xs']
    post_url = query_data[0]['post_url']
    comment_text = query_data[0]['comment_text']
    driver.get('https://d.facebook.com')
    driver.add_cookie({'name': 'c_user', 'value': user_id})
    driver.add_cookie({'name': 'xs', 'value': user_xs})
    driver.refresh()
    driver.get(post_url)
    time.sleep(3)
    #driver.find_element_by_css_selector('body').send_keys(Keys.END)
    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_DOWN)
    ActionChains(driver).move_to_element(driver.find_element_by_id('composerInput')).perform()
    driver.find_element_by_name('comment_text').send_keys(comment_text)
    time.sleep(1)
    driver.find_element_by_css_selector('input[value="Comment"]').click()
    driver.save_screenshot('static/screen.png')
    
    
def get_screen():
    while True:
        driver.save_screenshot('static/screen.png')
        time.sleep(60)
        
task = Process(target=get_screen)
task.start()

from flask import Flask,request,render_template
PEOPLE_FOLDER = os.path.join('static')
app = Flask(__name__)
app.config['IMG'] = PEOPLE_FOLDER

@app.route('/')
def inx():
    return 'ok'


@app.route('/index')
def show_index():
    return 'ok'
    
    
    
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
    
@app.route('/ffb/like_post',methods = ["POST","GET"])
def api_like_post():
    try:
        if request.json != None:
            query_data = []
            query_data.append(request.json)
            task = Process(target=like_post,args = (query_data,))
            task.start()
            return "ok"
        else:
            return "OK"
    except:
        return 'nt'
    
@app.route('/ffb/comment_post',methods = ["POST","GET"])
def api_comment_post():
    try:
        if request.json != None:
            query_data = []
            query_data.append(request.json)
            task = Process(target=comment_post,args = (query_data,))
            task.start()
            return "ok"
        else:
            return "OK"
    except:
        return 'nt'
    
    
@app.route('/screen')
def ma():
    try:
        full_filename = os.path.join(app.config['IMG'], 'screen.png')
        return render_template("index.html", user_image = full_filename)
    except:
        return 'Error'

if __name__ == '__main__':
    app.run()
