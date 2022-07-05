import requests
from bs4 import BeautifulSoup
import random
import re
import time

# каждые пол часа делается запрос и копируются все айпи в файл "непроверенные айпи"
# списком их проверяем и рабочие сохраняем в файл "проверенные айпи"
# Когда все проверены - сохраняем список "проверенные айпи"  в базу данных
# Каждые полчаса проверяем базу, если не рабочий айпи - удаляем
# В БАЗЕ ПОСТОЯННО ДОЛЖНО БЫТЬ НЕ МЕНЕЕ 25 АЙПИ
# Если меньше - запускаем все эти функции

count = 0

headers = [
    {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"},
    {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"},
    {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"},
    {"User-Agent":"Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"},
]

header = random.choice(headers)

def proxie_checker(count):
    with open("unchecked_proxies.txt", "r") as file:
        text = file.read()
        proxies = text.split("\n")
        file.close()
    with open("checked_proxies.txt", "w") as file:
        for proxy in proxies:
            print("\nChecking proxy:", proxy)
            try:
                page = requests.get('https://ipecho.net/plain', timeout=3, proxies={"http": proxy, "https": proxy}, headers=header)
                print("Status OK, Output:", page.text)
                count += 1
                file.write(proxy+"\n")
            except OSError as e:
                print(e)
            print(count)
        file.close()


def site1_proxies_scrap():
    url = "https://www.sslproxies.org/"
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    text_field = soup.find('textarea', class_="form-control").text
    ls = text_field.split("\n")
    ls_1 = ls[3:-1]
    with open("unchecked_proxies.txt", 'w', encoding="utf-8") as file:
        for i in ls_1:
            file.write(i+"\n")
        file.close()

def site2_proxies_scrap():
    url = "https://free-proxy-list.net/#list"
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    text_field = soup.find('textarea', class_="form-control").text
    ls = text_field.split("\n")
    ls_2 = ls[3:-1]
    with open("unchecked_proxies.txt", 'a', encoding="utf-8") as file:
        for i in ls_2:
            file.write(i+"\n")
        file.close()

# def site3_proxies_scrap():
#     url = "https://proxyscrape.com/share/l5ty3b9"
#     r = requests.get(url, headers=header)
#     print('подключаемся к странице с ip', url)
#     time.sleep(3)
#     soup = BeautifulSoup(r.content, features="html.parser")
#     # print(soup)
#     text_field = soup.select("#proxyshare")
#     print(text_field)
#     for i in text_field:
#         text_field = i.text
#     ls = text_field.split("\n")
#     ls_3 = ls
#     with open("unchecked_proxies.txt", 'a', encoding="utf-8") as file:
#         for i in ls_3:
#             file.write(i+"\n")

def main():
    site1_proxies_scrap()
    # site2_proxies_scrap()
    # site3_proxies_scrap()
    proxie_checker(count)

main()




