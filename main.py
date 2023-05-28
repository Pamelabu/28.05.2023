import pandas as pd
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://luzceramics.com/")
time.sleep(3)
przycisk_akceptuj = driver.find_element(By.XPATH, '//*[@id="PopupSignupForm_0"]/div[2]/div[1]')
przycisk_akceptuj.click()
time.sleep(3)

przycisk_sklep = driver.find_element(By.XPATH, '//*[@id="menu-item-181"]/a')
przycisk_sklep.click()
time.sleep(3)

nazwy_produktow = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__title')

# for produkt in nazwy_produktow:
#     print(produkt.text)

nazwy_oczyszczone = []
for produkt in nazwy_produktow:
    nazwy_oczyszczone.append(produkt.text)
    # print(nazwy_oczyszczone)
time.sleep(5)
ceny_produktow = driver.find_elements(By.CLASS_NAME, 'price')
ceny_oczyszczone = []


for ceny in ceny_produktow:
    ceny_bez_waluty = ceny.text.lstrip('€')
    ceny_w_dobrym_formacie = ceny_bez_waluty.replace(',','.')
    ceny_w_poprawnym_formacie = float(ceny_w_dobrym_formacie)
    ceny_oczyszczone.append(ceny_w_poprawnym_formacie)
    print(ceny_oczyszczone)

    #129.50 dobre
    #129,5 złe python ogarnai kropkę nie przecinek


artykuly = {'names':nazwy_oczyszczone, 'prices':ceny_oczyszczone}
df_produkty = pd.DataFrame(artykuly)
print(df_produkty.head())

df_produkty['Status'] = 'Zapomnij'

df_produkty.loc[df_produkty['prices'] < 25, 'Status'] = 'Zainteresuj sie'

df_produkty.loc[(df_produkty['prices'] > 25) & (df_produkty['prices'] < 50), 'Status'] = 'Zaczekaj'

#loc wybiera wiersze które spełniają warunek 

print(df_produkty.head())

#laczenie z bazą danych sqlite

conn = sqlite3.connect('artykuly.sqlite')

df_produkty.to_sql('TabelaArtykulow', conn, if_exists='append', index=False) #zapisanie ramkki danych do tabeli w bazie danych
conn.close()


driver.quit()
