from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template, Response
from selenium.webdriver import ChromeOptions
import time

def get_frame():
    options=ChromeOptions()
    base='https://www.hackerrank.com'
    options.add_argument('--app={}'.format(base))
    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
    driver.fullscreen_window()
    tab_switches=0
    req_window_height,req_window_width=driver.get_window_rect()['height'],driver.get_window_rect()['width']
    time.sleep(5)
    rule_broken=False
    max_attempt=3
    exit_status=False
    while True:
        '''try:
            #driver.find_element_by_id('menu-item-2887').click()
            exit_status=True
        except:
            print('passed')
            pass'''
        curr_height,curr_width=driver.get_window_rect()['height'],driver.get_window_rect()['width']
        if curr_height<req_window_height or curr_width<req_window_width:
            tab_switches+=1
            driver.fullscreen_window()
        if tab_switches>max_attempt:
            rule_broken=True
        if rule_broken or exit_status:
            break
    if rule_broken==True:
        driver.quit()
        return '0'
    else:
        driver.quit()
        return '1'

def result(res):
    if res=='0':
        print('rule toda hai aapne')
    elif res=='1':
        print('success...')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calc')
def calc():
    m=Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
    r=m.data.decode("utf-8")
    result(r)
    return m

if __name__ == '__main__':
    app.run(host="localhost",debug=True)
