from selenium import webdriver
import os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

pasta_downloads = str(Path.home() / "Downloads")
prefs = {
    "download.default_directory": pasta_downloads,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

load_dotenv("key.env")

amdinemail = os.getenv("loginadmin")
mobzila = os.getenv("macacopreto")

driver = webdriver.Chrome()

driver.get("https://oyasumi-web.github.io/Controle-Vencimentos/")

#Colocando Email
input_email = driver.find_element(By.ID, "em")
input_email.send_keys(amdinemail)

input_pass = driver.find_element(By.ID, "pw")
input_pass.send_keys(mobzila) 

btn_go = driver.find_element(By.ID, "go")
btn_go.send_keys(Keys.ENTER)


time.sleep(5)

relatorio_btn = driver.find_element(By.XPATH, '//button[@data-t="rel"]')
relatorio_btn.click()
time.sleep(1)

filtro_mes = driver.find_element(By.XPATH, '//*[@id="app"]/nav/button[2]')
filtro_mes.click()
time.sleep(1)


mes1_aba = driver.find_element(By.XPATH, '//*[@id="rel-m"]/option[2]')
mes1_aba.click()
time.sleep(1)

btn_exportar_excel = driver.find_element(By.ID, "xl-rel")
btn_exportar_excel.click()
time.sleep(2)


