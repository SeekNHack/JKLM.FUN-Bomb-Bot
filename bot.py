from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import random
from selenium.common.exceptions import TimeoutException


if len(sys.argv) < 4:
    print("Usage: python script.py [link] [it/eng] [username]")
    exit()
file = open(f"{sys.argv[2]}.txt",'r').readlines()
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get(sys.argv[1])

def searchWord(wordlist,letters):
    for word in wordlist:
        if letters in word:
            return word
    return None

def chooseWord(letters):
    start = random.randint(0,len(file)//2)
    end = random.randint(len(file)//2+1,len(file))
    list = file[start:end]
    word = searchWord(list,letters)
    tries=0
    while word == None:
        word = searchWord(list,letters)
        start = random.randint(0,len(file)//2)
        end = random.randint(len(file)//2+1,len(file))
        list = file[start:end]
        tries=tries+1
        if tries==1000:
            return None
    return word


def login():
    wait = WebDriverWait(driver,60)
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/form")))
    name = driver.find_element("xpath", "/html/body/div[2]/div[3]/form/div[2]/input")
    name.clear()
    name.send_keys(sys.argv[3])
    name.send_keys(Keys.ENTER)

def join():
    wait = WebDriverWait(driver,120)
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[4]/div[1]")))
    iframe = driver.find_element("xpath", "/html/body/div[2]/div[4]/div[1]/iframe")
    driver.switch_to.frame(iframe)
    joined=False
    while not joined:
        try:
            wait = WebDriverWait(driver,10)
            wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div[1]/div[1]/button")))
            button = driver.find_element("xpath", "/html/body/div[2]/div[3]/div[1]/div[1]/button")
            button.click()
            joined=True
        except TimeoutException:
            print("waiting for joining")
            continue
            

def getLetters():
    letters= driver.find_element("xpath", "/html/body/div[2]/div[2]/div[2]/div[2]/div")
    return letters.text.lower()

def sendWord(word):
    form =driver.find_element("xpath", "/html/body/div[2]/div[3]/div[2]/div[2]/form/input")
    form.send_keys(word)
    form.send_keys(Keys.ENTER)

def myTurn():
    wait = WebDriverWait(driver,60)
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div[2]/div[2]")))

def start():
    login()
    join()
    while True:
        try:
            myTurn()
            time.sleep(round(random.uniform(0.5,1),1))
            letters = getLetters()
            word = chooseWord(letters)
            if word==None:
                continue
            sendWord(word)
            button = driver.find_element("xpath", "/html/body/div[2]/div[3]/div[1]/div[1]/button")
            if button!=null:
                button.click()
        except:
            continue

start()
