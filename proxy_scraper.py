import random
import time
import requests
from bs4 import BeautifulSoup
import threading

# каждый час делается запрос и копируются все айпи в файл "непроверенные айпи"
# списком их проверяем и рабочие сохраняем в файл "проверенные айпи"
# Когда все проверены - сохраняем список "проверенные айпи"  в базу данных
# Каждые полчаса проверяем базу, если не рабочий айпи - удаляем
# В БАЗЕ ПОСТОЯННО ДОЛЖНО БЫТЬ НЕ МЕНЕЕ 25 АЙПИ
# Если меньше - запускаем все эти функции вне очереди

# Сделать в админке кнопку "Дать подписку"
# В моделе Profile добавить поле paid_until
# По нажатию - + 9999 баланса и paid_until + 30days
# Каждый день проверять поле paid_until
# if current_date < paid_until => -9999 баланса, либо, если меньше 9999 = -весь баланс
# Сделать в админке кнопку "Дать баланс"

count = 0

headers = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"},
    {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"},
    {"User-Agent": "Microsoft Internet Explorer 6 / IE 6: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"},
    {"User-Agent": "Microsoft Internet Explorer 7 / IE 7: Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)"},
]

header = random.choice(headers)

def site_proxies_scrap(url):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    text_field = soup.find('textarea', class_="form-control").text
    ls = text_field.split("\n")
    ls_1 = ls[3:-1]
    with open("unchecked_proxies.txt", 'a', encoding="utf-8") as file:
        for i in ls_1:
            file.write(i+"\n")
        file.close()

def site1_proxies_scrap(url):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    ls = str(soup.text).replace("\r", '').split("\n")
    ls_1 = ls[:-1]
    print(ls_1)
    with open("unchecked_proxies.txt", 'a', encoding="utf-8") as file:
        for i in ls_1:
            file.write(i+"\n")
        file.close()


def doubler(proxy, ):
    with open('checked_proxies.txt', 'a', encoding='utf-8') as file:
        try:
            page = requests.get('https://ipecho.net/plain', timeout=3, proxies={"http": proxy, "https": proxy}, headers=header)
            file.write(proxy + '\n')
            print('Status OK: ', proxy)
        except OSError as e:
            pass
            print(e, proxy)


if __name__ == '__main__':
    with open('checked_proxies.txt', 'w', encoding='utf-8') as file:
        file.close()
    with open('unchecked_proxies.txt', 'w', encoding='utf-8') as file:
        file.close()
    site_proxies_scrap("https://www.sslproxies.org/")
    site_proxies_scrap("https://free-proxy-list.net/#list")
    site_proxies_scrap("https://free-proxy-list.net/anonymous-proxy.html")
    # site1_proxies_scrap("https://api.proxyscrape.com/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")

    with open('unchecked_proxies.txt', 'r', encoding='utf-8') as file:
        proxies = file.read().split("\n")
        file.close()
    for proxy in proxies:
        try:
            my_thread = threading.Thread(target=doubler, args=(proxy, ))
            my_thread.start()
        except:
            time.sleep(3)
            my_thread = threading.Thread(target=doubler, args=(proxy,))
            my_thread.start()


