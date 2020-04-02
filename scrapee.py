# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 19:13:15 2018

@author: User
"""
import csv
import urllib as url
import time
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.common.by import By
import random

def url_lib(dest_url):
    #content = url.request.urlopen(dest_url)
    req = url.request.Request(
            dest_url,
            data=None,
            headers = {
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            }
            )
    with url.request.urlopen(req) as response:
        content = response.read()
        print(content)
    
def selenium(dest_url):
    browser = webdriver.Firefox()
    #browser.get(dest_url)
    score = browser.find_element_by_class_name('score')
    print(score)
    
def selenium2(dest_url):
    with closing(webdriver.Firefox()) as browser:
        browser.get(dest_url)
        #print (browser.find_element_by_xpath("html").text)
        print ("Scraping: >>'" + dest_url + "'<<")
        print ("Rating:")
        print (browser.find_element_by_class_name('score').text)
        element = browser.find_element_by_class_name('item-image-actual')
        print("src:")
        print(element.get_attribute("src"))
        element = browser.find_element_by_class_name('stream-next')
        element.click()
        print(browser.find_element_by_xpath("html").text) 

def harvestPr0(num, start_url, save_steps=30, speed_modificator=1):
    data = []
    score, element, content_url, next_button, tag_link, tags = "", "", "", "", "", []
    with closing(webdriver.Firefox()) as browser:
        browser.get(start_url)
        last_content_url = ""
        for i in range(num):
            try:
                score = browser.find_element_by_class_name('score').text
                element = browser.find_element_by_class_name('item-image-actual')
                content_url = element.get_attribute("src")
                try:
                    user = browser.find_element_by_class_name('user').text
                except:
                    user = "deleted"
                tag_link = browser.find_elements_by_class_name('tag-link')
                tags = [tag.text for tag in tag_link if tag.text != ""]
                # only save new stuff
                if last_content_url != content_url:
                    data.append([browser.current_url, content_url, score, tags, user])
                #refresh if stuck
                else:
                    "Browser was stuck, scrolling the page..."
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("---------------------")
                last_content_url = content_url
                    
            except:
                print("no such element / scraping this image failed")
                print("---------------------")
                save_content(data)
                save("scrape_data/last_url.txt", browser.current_url)
                data = []
                                            
            print ("Scraping #" + str(i) + ": \n" + browser.current_url + "'<<")
            print ("Rating:\n"+score)
            print ("User:\n"+user)
            print ("Tags:\n", tags)
            print("src:\n" + content_url)
            print("---------------------")
            
            next_button = browser.find_element_by_class_name('stream-next')
            next_button.click()
            if i == num-1 or i%save_steps == 0:
                print("Saving Progress...")
                print("Data:", data)
                save("scrape_data/last_url.txt", browser.current_url)
                save_content(data)
                data=[]
                print("-----------------------")
            time.sleep(speed_modificator * random.choice([0.75,0.85,0.95,1.05,1.2,1.3]))
        return data
    
def save_content(content, filename="scrape_data/pr0Data4.csv"):
    try:    
        with open(filename, "a", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator="\n")
            writer.writerows(content)
    except:
        print("Error while trying to save the content!")

def save(filename, content):
    try:
        with open(filename, "w") as output:
            output.write(content)
    except:
        print("Error while saving")

def load_url(pathToFile="scrape_data/last_url.txt"):
    with open(pathToFile, "r") as file:
        return file.readlines()[0]
       
#url_lib("https://pr0gramm.com/top/2782197")
#selenium("https://pr0gramm.com/top/2794619")
#selenium2("https://pr0gramm.com/top/2794619")
"""
for i in range(8):
    try:
        print(harvestPr0(random.randrange(10,150,1),load_url()))
    except:
        pass
    time.sleep(random.randrange(3,20,1))
 """   
#save_content("test.csv", [["1234", "42"],["porno.de", 100]])
#save("scrape_data/last_url.txt", "https://pr0gramm.com/top/2795493")
#print(load("scrape_data/last_url.txt"))
harvestPr0(2000,load_url(),50, 0.5)

