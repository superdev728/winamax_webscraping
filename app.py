from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from flask import Flask
from supabase_py import create_client
# from supabase_realtime import create_client as create_realtime_client
# import supabase_realtime
# from flask_ngrok import run_with_ngrok

supabase_url = 'https://knybnecfagfyrfkxojbi.supabase.co'
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtueWJuZWNmYWdmeXJma3hvamJpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTE0NTU4NDQsImV4cCI6MjAwNzAzMTg0NH0.9302F79pVTzOclwWlHmfkyC74tBRU5josyjBZXUuYZY"

supabase = create_client(supabase_url, supabase_key)

driver=[0,0]
parent_div=[0,0]
hide_btn_checked=[False]

options=webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver[0] = uc.Chrome(options=options)

def first_func():
    driver[0].get("https://www.winamax.fr/poker/launch_poker.php")
    url = 'https://www.winamax.fr/poker/launch_poker.php'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    
    iframe = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='pokWEB']")))
    driver[0].switch_to.frame(iframe)

    iframe1 = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mount']/div[1]/div/div[3]/div[1]/div[2]/div/iframe")))
    driver[0].switch_to.frame(iframe1)

def enter_to_cash_game_frame():
    login_email = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mount']/div[2]/form/div/div[1]/div[2]/div[2]/input")))
    time.sleep(0.5)
    login_email.clear()
    login_email.send_keys("bed36627@gmail.com")
    time.sleep(0.5)

    login_psw = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mount']/div[2]/form/div/div[2]/input")))
    time.sleep(0.5)
    login_psw.send_keys('bed36627')

    button = WebDriverWait(driver[0], 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mount']/div[2]/form/button/div/div[1]/div")))
    button.click()

    iframe3 = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='pokWEB']")))
    driver[0].switch_to.frame(iframe3)

    cash_came = WebDriverWait(driver[0], 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mount']/div/div[2]/div/div/div/div[9]/div[1]/div[3]")))
    cash_came.click()
    time.sleep(5)

    if hide_btn_checked[0]:
        pass
    else:
        hide_empty_game=WebDriverWait(driver[0],60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='isEmptyGamesSelected']")))
        hide_empty_game.click()
        hide_btn_checked[0]=True
    time.sleep(5)

    parent_div[0] = WebDriverWait(driver[0], 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mount']/div/div[2]/div/div/div/div[9]/div[2]/div/div[1]/div[3]/div")))

def get_data_from_list():
    json_data=[{"info":"info", "info": "info"}]
    while True:
        
        room_lists=parent_div[0].find_elements(By.CSS_SELECTOR, ".pkr__sc-5uy1cr-20.hwtUbS")
        type_lists=parent_div[0].find_elements(By.CSS_SELECTOR, ".pkr__wpq7md-0.pkr__sc-5uy1cr-1.pkr__sc-5uy1cr-14.coNlvg.caPsxh.ezXtk")
        blind_lists=parent_div[0].find_elements(By.CSS_SELECTOR, ".pkr__wpq7md-0.pkr__sc-5uy1cr-1.pkr__sc-5uy1cr-4.pkr__sc-5uy1cr-6.eOjJey.bbeeak.hOQoEp.ktqzQT")
        
        room_elements=[]
        type_elements=[]
        
        room_list=room_lists[len(room_lists)-1]
        type_list=type_lists[len(room_lists)-1]
        blind_list=blind_lists[len(room_lists)-1]
        room_list_text = room_list.text
        type_list_text = type_list.text
        blind_list_text = blind_list.text

        data_line={"Tablename:": room_list_text, "Typename:": type_list_text, "Blind:": blind_list_text, "Nicknames:": [n.text for n in driver[0].find_elements(By.CSS_SELECTOR, ".pkr__sc-826dy9-3.cUPamy")]}

        if data_line ==json_data[-1]:
            break

        for i in range(len(room_lists)):
            room_list=room_lists[i]
            type_list=type_lists[i]
            blind_list=blind_lists[i]
            room_list_text=room_list.text
            type_list_text=type_list.text
            blind_list_text=blind_list.text
            room_list.click()
            a=0
            while True:
                try:
                    if driver[0].find_elements(By.CSS_SELECTOR, ".pkr__sc-826dy9-3.cUPamy"):
                        break
                except:
                    a+=1
                    if a == 500:
                        print(a)
                        break
                    else:
                        pass
            if a==500:
                continue
            data_line={"Tablename:": room_list_text, "Typename:": type_list_text, "Blind:": blind_list_text, "Nicknames:": [n.text for n in driver[0].find_elements(By.CSS_SELECTOR, ".pkr__sc-826dy9-3.cUPamy")]}

            if data_line not in room_elements:
                room_elements.append(data_line)
            driver[0].execute_script("arguments[0].scrollIntoView(true);", room_list)
        if room_elements not in json_data:
            json_data +=room_elements

    return json_data
    
def sec_func():
    first_func()
    while True:
        try:
            enter_to_cash_game_frame()
            break
        except Exception as e:
            print(e)

def get_data():
    while True:
        try:
            time.sleep(5)
            json_data = get_data_from_list()
            json_data.pop(0)
            
            # Insert the data into Supabase
            table_name = 'easystack_table'
            supabase.table(table_name).upsert(json_data).execute()
            
        except Exception as e:
            print(e)
            break
        except TimeoutException:
            print("Timeout occurred while waiting for an element to be visible or clickable")
        except NoSuchElementException:
            print("Unable to locate element.")

while True:
    sec_func()
    get_data()
        

