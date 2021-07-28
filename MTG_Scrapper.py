from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from PIL import Image
import os

# make sure this path is correct
def startChrome():
    PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    return driver

def readCards():
    with open("MTGCards.txt") as f:
        cards = [line.rstrip() for line in f]

    for card in cards:
        print(card)
    return cards

# print("Add to cart button found")

def mtgArtScrapper(card):
    driver.get(mtgArtLink)

    searchField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.search_input")))
    searchField.send_keys(card.replace("'", " ") + "\n")

    print("Finding Image from MTG Art")
    # Show image
    try:
        imageBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/div/table/tbody/tr/td[3]/div/div[2]/a")))
        imageBtn.click()
    except:
        print("No Button to click")

    # Pause
    input("When ready press Enter\n\n")

    print("Downloading Image from MTG Art")
    try:
        imageTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/img")))
        src = imageTag.get_attribute('src')
        print(src)

        imageData = requests.get(src).content
        with open(imgFolder + os.path.sep + card + ".jpg", "wb") as handler:
            handler.write(imageData)
        # Convert to PNG
        jpg = Image.open(imgFolder + os.path.sep + card + ".jpg")
        jpg.save(imgFolder + os.path.sep + card + ".png")
    except:
        print("No Image to download from MTG Art")
        scryFallImageScrapper(card)

def scryFallScrapper(card):
    print("Finding Text on from ScryFall")
    driver.get(scryFallLink)
    
    searchField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#q.homepage-form-field")))
    searchField.send_keys(cards[i] + "\n")

    print("Reading Text from ScryFall")
    try:
        oracleTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-text-oracle>p")))
        oracleText = oracleTag.text
        flavorTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-text-flavor>p")))
        flavorText = flavorTag.text
        print(card)
        print(oracleText)
        print(flavorText)

        # Save Text
        with open(textFolder + os.path.sep + card + ".txt", "w") as handler:
            handler.write(oracleText + os.linesep + flavorText)

    except:
        print("No text to download")

    # Pause
    input("When ready press Enter\n\n")

def scryFallImageScrapper(card):
    print("Finding image")
    driver.get(scryFallLink)
    
    searchField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#q.homepage-form-field")))
    searchField.send_keys(cards[i] + "\n")

    print("Downloading image from ScryFall")
    try:
        imageTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/ul/li[2]/a")))
        src = imageTag.get_attribute('href')

        print(src)

        imageData = requests.get(src).content
        with open(imgFolder + os.path.sep + card + ".jpg", "wb") as handler:
            handler.write(imageData)
        # Convert to PNG
        jpg = Image.open(imgFolder + os.path.sep + card + ".jpg")
        jpg.save(imgFolder + os.path.sep + card + ".png")

    except:
        print("No image to download from ScryFall")

    # Pause
    input("When ready press Enter\n\n")


imgFolder = "images_3"
if not os.path.exists(imgFolder):
    os.makedirs(imgFolder)

textFolder = "text_3"
if not os.path.exists(textFolder):
    os.makedirs(textFolder)

mtgArtLink = "https://www.mtgpics.com/index"
scryFallLink = "https://scryfall.com/"
driver = startChrome()
cards = readCards()
try:
    for i in range(10, 13):
        print("Card Number: " + str(i) + " - " + cards[i])
        # Get Art
        mtgArtScrapper(cards[i])
        # Get Text
        scryFallScrapper(cards[i])
    print("Finished!")
finally:
    driver.close()
