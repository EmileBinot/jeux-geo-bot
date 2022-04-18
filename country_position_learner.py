from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

import cv2
import csv
from matplotlib import pyplot as plt

import pandas as pd

# Initialize the webdriver
options = Options()
options.add_extension(r'.\extensions\1.42.4_1.crx')
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

# Open the websitet
browser.get('https://www.jeux-geographiques.com/jeux-en-ligne-Jeu-Pays-d-Afrique-_pageid158.html')
cookies_button = browser.find_element(By.XPATH, "//button[text()=\"J'ACCEPTE\"]").click()
browser.execute_script("document.getElementById('canvas').scrollIntoView();")
browser.find_element(By.ID,'buttonStartWithoutTimer').click()
time.sleep(2) # wait for map appear
browser.save_screenshot("bg_africa.PNG") # save background for diff later

class Country: 
    def __init__(self, name, cX, cY): 
        self.name = name 
        self.cX = cX
        self.cY = cY
        
def get_country_position():
    action = ActionChains(browser)
    canvas = browser.find_element(By.ID,'canvas')
    action.move_to_element_with_offset(canvas,0,0).click().perform()
    time.sleep(0.1)
    action.move_to_element_with_offset(canvas,0,0).click().perform()
    time.sleep(0.1)
    action.move_to_element_with_offset(canvas,0,0).click().perform()
    time.sleep(0.4)
    browser.save_screenshot("screenshot.PNG")

    background = cv2.imread('bg_africa.PNG',0)[y:y+h, x:x+w]
    after = cv2.imread('screenshot.PNG',0)[y:y+h, x:x+w]

    diff = cv2.absdiff(background, after)
    ret,thresh = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)
    canny_edges = cv2.Canny(thresh, 30, 200)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

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

    return cX, cY

countryList = []

for i in range(56):
    time.sleep(1) # wait for country name to appear
    name = browser.find_element(By.ID,'questionTextLabel').text
    if country not in countryList:
        print("Country not in list")
        cX, cY = get_country_position()
        countryList.append(Country(name, cX, cY))
    else:
        print("Country already in list")
        cX, cY = countryList[i].cX, countryList[i].cY





# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

# import time

# import cv2
# import csv
# from matplotlib import pyplot as plt

# import pandas as pd

# options = Options()

# options.add_extension(r'.\extensions\1.42.4_1.crx')
# options.add_argument("--start-maximized")
# options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 1 
# })

# # option.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

# # Open the Website
# browser.get('https://www.jeux-geographiques.com/jeux-en-ligne-Jeu-Pays-d-Afrique-_pageid158.html')
# cookies_button = browser.find_element(By.XPATH, "//button[text()=\"J'ACCEPTE\"]").click()

# browser.execute_script("document.getElementById('canvas').scrollIntoView();")
# browser.find_element(By.ID,'buttonStartWithoutTimer').click()
# time.sleep(2) # wait for map appear
# browser.save_screenshot("bg_africa.PNG") # save background for diff later


# class Country: 
#     def __init__(self, name, cX, cY): 
#         self.name = name 
#         self.cX = cX
#         self.cY = cY

# countryListdf = pd.read_csv('africa.csv')
# headers =  ["country", "Xcentroid", "Ycentroid"]
# countryListdf.columns = headers
# print(countryListdf)
# countryList=[]

# for i in range(56):
    
#     time.sleep(1) # wait for country name to appear
#     country = browser.find_element(By.ID,'questionTextLabel').text

    
#     if country not in countryListdf.country.values:
#         print("Country not found in database")

#         action = ActionChains(browser)
#         canvas =browser.find_element(By.ID,'canvas')
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         time.sleep(0.1)
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         time.sleep(0.1)
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         time.sleep(0.4)
#         browser.save_screenshot("screenshot.PNG")

#         x=500
#         y=165
#         w=1125 # width of the canvas
#         h=750 # height of the canvas
#         background = cv2.imread('bg_africa.PNG',0)[y:y+h, x:x+w]
#         after = cv2.imread('screenshot.PNG',0)[y:y+h, x:x+w]

#         diff = cv2.absdiff(background, after)
#         ret,thresh = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)
#         canny_edges = cv2.Canny(thresh, 30, 200)
#         contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#         cXlist=[]
#         cYlist=[]
        
#         for c in contours:
#             # calculate moments for each contour
#             M = cv2.moments(c)
#             if M["m00"] != 0:
#                 cX = int(M["m10"] / M["m00"])
#                 cY = int(M["m01"] / M["m00"])
#                 cXlist.append(cX)
#                 cYlist.append(cY)

#             else:
#                 cX, cY = 0, 0

#         print(country)      
#         if len(cXlist) > 0:
#             countryList.append([country, cXlist[0], cYlist[0]])
#             cv2.circle(canny_edges, (cXlist[0], cYlist[0]), 5, (255, 0, 0), -1)
#             cv2.putText(canny_edges, "centroid", (cXlist[0] - 25, cYlist[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
#             # print(len(cXlist))
#             print(cXlist[0])
#             print(cYlist[0])

#         else:
#             print("no contour found")
#             countryList.append([country, 0, 0])
#         plt.imshow(canny_edges)
#         plt.show()
#         print("\n")
#     else :
#         # country_data = countryListdf.loc(country)
#         print("Country found in database")
#         print(country)
#         print("\n")
#         action = ActionChains(browser)
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         time.sleep(0.1)
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         time.sleep(0.1)
#         action.move_to_element_with_offset(canvas,0,0).click().perform()
#         # action = ActionChains(browser)
#         # canvas = browser.find_element(By.ID,'canvas')
#         # action.move_to_element_with_offset(canvas,country_data["Xcentroid"],country_data["Ycentroid"]).click().perform()
#         # time.sleep(0.1)
        


# print(pd.DataFrame(countryList))
# pd.DataFrame(countryList).to_csv('africa.csv')
