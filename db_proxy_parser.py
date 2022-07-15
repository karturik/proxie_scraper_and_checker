import sqlite3
import random
import time
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect(r'D:/kursy/project/grsmu_diplom/db.sqlite3')


## DB INSERT IP
# cur.execute("INSERT OR IGNORE INTO proxie_proxie (ip) VALUES ('192.156.22:34');")
# conn.commit()
# cur.execute("SELECT ip FROM proxie_proxie;")
# result = cur.fetchall()
# print(result)

## DB EXECUTE ALL IP
# cur.execute("SELECT ip FROM proxie_proxie;")
# result = cur.fetchall()
# ip_list = []
# for i in result:
#     ip_list.append(*i)
#     print(ip_list)

## DELETE BROKE IP
# cur.execute("DELETE FROM proxie_proxie WHERE ip='192.156.22:34';")
# conn.commit()
# cur.execute("SELECT ip FROM proxie_proxie;")
# result = cur.fetchall()
# print(result)


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

unchecked_proxies = []

def site_proxies_scrap(url, unchecked_proxies):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    text_field = soup.find('textarea', class_="form-control").text
    ls = text_field.split("\n")[3:-1]
    # ls_1 = ls[3:-1]
    unchecked_proxies += ls

def site1_proxies_scrap(url, unchecked_proxies):
    r = requests.get(url, headers=header)
    print('подключаемся к странице с ip', url)
    soup = BeautifulSoup(r.content, features="html.parser")
    ls = str(soup.text).replace("\r", '').split("\n")[:-1]
    # ls_1 = ls[:-1]
    unchecked_proxies += ls

checked_proxies = []

def doubler(proxy, checked_proxies):
    try:
        page = requests.get('https://ipecho.net/plain', timeout=2, proxies={"http": proxy, "https": proxy}, headers=header)
        checked_proxies.append(proxy)
        print('Status OK: ', proxy)
    except OSError as e:
        pass
        print(e, proxy)

if __name__ == '__main__':
    site_proxies_scrap("https://www.sslproxies.org/", unchecked_proxies)
    # site_proxies_scrap("https://free-proxy-list.net/#list", unchecked_proxies)
    # site_proxies_scrap("https://free-proxy-list.net/anonymous-proxy.html", unchecked_proxies)
    # site1_proxies_scrap("https://api.proxyscrape.com/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")

    for proxy in unchecked_proxies:
        try:
            doubler(proxy, checked_proxies)
        except:
            pass
    print(checked_proxies)

cur = conn.cursor()

for item in checked_proxies:
    cur.execute(f"INSERT OR IGNORE INTO proxie_proxie (ip) VALUES ('{item}');")
conn.commit()
cur.execute("SELECT ip FROM proxie_proxie;")
result = cur.fetchall()
print(result)