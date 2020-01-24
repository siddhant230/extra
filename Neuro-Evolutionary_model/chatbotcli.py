import random
import speech_recognition as sr
from selenium import webdriver
import numpy as np
import wolframalpha,pyttsx3,json,nltk
from nltk.stem.lancaster import LancasterStemmer
import datetime,wikipedia,time,smtplib,warnings
from sklearn.externals import joblib
#nltk.download('punkt')

warnings.filterwarnings('ignore')
engine=pyttsx3.init('sapi5')
client=wolframalpha.Client('JGQG46-Y5WTEL7J5G')
voice=engine.getProperty('voices')
stemmer=LancasterStemmer()

engine.setProperty('voices',voice[len(voice)-2].id)
speed=200
message=''
neg=1
engine.setProperty('rate', speed)
options = webdriver.ChromeOptions()
with open('C:\\Users\\tusha\Desktop\json file\\intents2.json') as f:
    data=json.load(f)

model=joblib.load('C:\\Users\\tusha\Downloads\chat_bot.pkl')
words=joblib.load('C:\\Users\\tusha\Downloads\words.pkl')
labels=joblib.load('C:\\Users\\tusha\Downloads\labels.pkl')

#######nlp work##########
def bag_of_words(s,words):
  bag=[0 for _ in range(len(words))]

  s_words=nltk.word_tokenize(s)
  s_words=[stemmer.stem(w.lower()) for w in s_words]

  for se in s_words:
    for i,w in enumerate(words):
      if w==se:
        bag[i]=1
  return bag
###########model here#######################
def reply(text_inp):
    res='I am sorry, I cannot answer that...'
    result=model.predict([bag_of_words(text_inp,words)])
    result_ind=np.argmax(result)
    tag=labels[result_ind]

    for tg in data['intents']:
      if tg['tag'] == tag:
        res=tg['responses']
    speak(random.choice(res))
############model here#####################

def speak(text):
    print('BOT : '+text)
    engine.say(text)
    engine.runAndWait()
c=0
stop,playing=False,1
def listen():
    global stop,playing
    global c,speed,neg
    r=sr.Recognizer()
    text=''
    if stop==False:
        if neg==-1:
            speak('NOW START!')
        else:
            speak('How can I help?')
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
        except:
            c+=1
            err="I can't understand what you said sir,Please try again..."
            if stop==False:
                speak(err)
                if c==2:
                    err="Try writing your query..."
                    speak(err)
                    text=input('YOU : ')
    if text!='' and stop==False:
        c=0
        print('YOU : {}'.format(text))
        commands=text.split(' ')
        for i in range(len(commands)):
            commands[i]=commands[i].lower()
        if 'speak' in commands and 'fast' in commands and stop==False:
            speak('Speeding myself up!!')
            speed=min(600,50+speed)
            engine.setProperty('rate', speed)
        elif ('email' in commands and 'write' in commands) or neg==-1 and stop==False:
            write_email(commands)
        elif 'speak'in commands and 'slow' in commands and stop==False:
            speak('Slowing myself down!!')
            speed=max(50,abs(50-speed))
        elif 'wait' in commands and stop==False:
            speak('I am waiting...')
            time.sleep(5)
            speak('I waited for 5 seconds...')
        elif 'stop' in commands:
            speak('STOPPING')
            stop=True
        elif 'start' in commands:
            speak('STARTING')
            stop=False
        elif 'f***' in commands and stop==False:
            speak('denge pel khatam ho jayga khel...')
            speak('Please atleast talk good, kharaab to apki shakal bhi hai...(#offence Intended)')
        elif 'weather' in commands and stop==False:
            weather(commands)
        elif 'quit' in commands and stop==False:
            quitter()
        elif 'open' in commands or 'run' in commands and stop==False:
            run_command(commands)
        elif ('play' in commands or 'pause' in commands) and stop==False:
            play_song(commands)
        elif 'search' in commands or 'joke' in commands and stop==False:
            search_command(commands)
        elif stop==False:
            reply(text)

def quitter():
    global driver,driver2,playing
    playing=1
    if driver!=None:
        driver.quit()
        driver=None
    elif driver2!=None:
        driver2.quit()
        driver2=None

recipent=''
def write_email(message=[]):
    global neg,recipent
    message=' '.join(message)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    neg*=-1
    if neg==-1:
        speak('Tell name of recipent')
        recipent=input('Recipent : ')
        speak('Now write the message')
        listen()
    elif neg==1:
        s.login('rsiddhant73@gmail.com','#pokemon911')
        s.sendmail('rsiddhant73@gmail.com',
                    recipent,msg=message)
        s.quit()
        speak('Email has been sent to => {}'.format(recipent))

button,driver=None,None
def play_song(commands):
    global button,playing,driver
    if 'quit' in commands and driver!=None and button!=None:
        playing=1
        driver.quit()
        button=None
        driver=None
    elif playing==1 and 'quit' not in commands:
        playing=-1
        id='https://www.soundcloud.com/search/sounds?q='
        driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
        name='%20'.join(commands[1:])
        driver.get(id+name)
        try:
            driver.find_element_by_class_name('search__empty')
            speak('No such song found sir,Try again...')
            driver.quit()
        except:
            button=driver.find_element_by_class_name('soundTitle__playButton')
            button.click()
    elif button!=None:
        button.click()
    else:
        speak('Nothing to Quit')

def weather(commands):
    query=' '.join(commands)
    speak("Searching for {}".format(query))
    result=client.query(query)
    opt=next(result.results).text
    speak(opt)

def search_command(commands):
    if 'joke' in commands:
        query='tell me a joke'
        result=client.query(query)
        opt=next(result.results).text
        opt=opt.split('(')[0]
        speak(opt)
    else:
        speak('searching...')
        if 'what' not in commands:
            query=' '.join(commands[1:])
        else:
            query=' '.join(commands)
        try:
            try:
                "BOT : Sure Sir!\nSearching for {}".format(query)
                speak("Searching for {}".format(query))
                result=client.query(query)
                opt=next(result.results).text
                speak("Here is what I found\nInternet says...")
                speak(opt)
            except:
                result=wikipedia.summary(query,sentences=3)
                speak("Here is what I found\nAccording to Wikipedia...")
                speak(result)
        except:
            browser=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
            speak("Here is what I found on Google...")
            browser.get("https://www.google.com/search?q=" + query + "&start=" + str(10 * 0))

driver2=None
def run_command(commands):
    global driver2
    if 'youtube' not in commands:
        speak('Opening {}'.format(''.join(commands[1:])))
        driver2=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
        driver2.get('https://www.{}.com'.format(''.join(commands[1:])))
    if 'youtube' in commands:
        speak('Opening {}'.format(''.join(commands[1:2])))
        if len(commands)<=2:
            driver2=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
            driver2.get('https://www.{}.com'.format(''.join(commands[1:])))
        else:
            driver2=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
            driver2.get("https://www.youtube.com/results?search_query={}".format(''.join(commands[4:])))
            time.sleep(3)
            driver2.find_element_by_id('video-title').click()

if __name__=='__main__':
    mode='#'
    times=datetime.datetime.now().hour
    if times>=0 and times<12:
        speak('Good Morning Sir!')
    elif times>=12 and times<=16:
        speak('Good Afternoon Sir!')
    elif times>16 and times<20 and times!=0:
        speak('Good Evening Sir!')
    else:
        speak("It's already Night")

    while mode=='#':
        listen()
