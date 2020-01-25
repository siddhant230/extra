from flask import Flask,render_template,redirect,request,url_for,Response
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
import time,pickle,re

pattern=re.compile('[.a-zA-Z]+[0-9]*@gmail.com')
app=Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method=="POST":
		name=request.form["text"]
		password=request.form["pass"]
		if name=="sid" and password=="1234":
			res=Response(take_test(name,password))
			res=res.data.decode("utf-8")
			print(res)
			if res=='1':
				return redirect(url_for("user",name="good job"))
			else:
				return redirect(url_for("user",name="tried to cheat??"))

		else:
			return render_template('login.html',content="wrong credentials")
	else:
		return render_template('login.html',content="")

@app.route("/register",methods=["POST","GET"])
def register():
	if request.method=="POST":
		password=request.form["pass"]
		conf_password=request.form["confpass"]
		email=request.form['email']
		correct=False
		if re.findall(pattern=pattern,string=email)==[]:
			return render_template('register.html',content="Invalid E-mail")
		else:
			correct=True
		if password==conf_password and correct:
			return redirect(url_for("user",name="SUCCESSFULLY REGISTERED"))
		else:
			return render_template('register.html',content="password and confirm password didn't matched")
	else:
		return render_template('register.html',content='')

@app.route("/about_us")
def about_us():
	return render_template('about_us.html')

def take_test(name,password):
	options = ChromeOptions()
	base = 'C:\\Users\\tusha\Desktop\\flask_app_create\webapp_flask\\templates\\test.html'
	options.add_argument('--app={}'.format(base))
	driver = webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe', options=options)
	driver.fullscreen_window()
	tab_switches = 0
	req_window_height, req_window_width = driver.get_window_rect()['height'], driver.get_window_rect()['width']
	exp_url=driver.current_url
	#time.sleep(2)
	rule_broken = False
	max_attempt = 3
	exit_status = False
	text_grabbed=''
	while driver.current_url==exp_url:
		if driver.current_url!=exp_url:
			break
		try:
			text_grabbed=driver.find_element_by_tag_name('textarea').get_attribute('value')
		except:
			pass
		curr_height, curr_width = driver.get_window_rect()['height'], driver.get_window_rect()['width']
		if curr_height < req_window_height or curr_width < req_window_width:
			tab_switches += 1
			driver.fullscreen_window()
		if tab_switches > max_attempt:
			rule_broken = True
		if rule_broken or exit_status:
			break
	obj={name:text_grabbed}
	print(obj)
	f=open('test_opt.pkl','wb')
	pickle.dump(obj,f)
	f.close()

	if rule_broken == True:
		driver.quit()
		return '0'
	else:
		driver.quit()
		return '1'

@app.route("/<name>")
def user(name):
	return render_template('redirecter.html',content=name)

@app.route('/admin')
def admin():
	password=input('enter here : ')
	if password=='sid':
		return 'welcome to admin page'
	else:
		return 'access denied'

if __name__=='__main__':
	app.run(debug=True)
