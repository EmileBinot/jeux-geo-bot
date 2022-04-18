from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

options = Options()

options.add_extension(r'.\extensions\1.42.4_1.crx')
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

# option.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

# Open the Website
browser.get('https://www.jeux-geographiques.com/jeux-en-ligne-Jeu-Pays-d-Afrique-_pageid158.html')
cookies_button = browser.find_element(By.XPATH, "//button[text()=\"J'ACCEPTE\"]").click()

browser.execute_script("document.getElementById('canvas').scrollIntoView();")
browser.find_element(By.ID,'buttonStart').click()
time.sleep(2) # wait for country name to appear
country = browser.find_element(By.ID,'questionTextLabel').text
print("country:",country)

browser.save_screenshot("bg_africa.PNG") # save background for diff later
action = ActionChains(browser)
canvas =browser.find_element(By.ID,'canvas')
action.move_to_element_with_offset(canvas,0,0).click().perform()
time.sleep(0.1)
action.move_to_element_with_offset(canvas,0,0).click().perform()
time.sleep(0.1)
action.move_to_element_with_offset(canvas,0,0).click().perform()
time.sleep(0.4)
browser.save_screenshot("screenshot.PNG")

# importing required libraries
import cv2
from matplotlib import pyplot as plt


# reads an input image
# x=397 
x=500
y=165
w=1125 # width of the canvas
h=750 # height of the canvas
background = cv2.imread('bg_africa.PNG',0)[y:y+h, x:x+w]
after = cv2.imread('screenshot.PNG',0)[y:y+h, x:x+w]

diff = cv2.absdiff(background, after)
ret,thresh = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cXlist=[]
cYlist=[]
for c in contours:
    # calculate moments for each contour
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cXlist.append(cX)
        cYlist.append(cY)
    else:
        cX, cY = 0, 0

i=0
print(cXlist[i])
print(cYlist[i])

plt.imshow(thresh)
plt.show()

while True :
    pass

