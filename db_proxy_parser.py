import sqlite3

conn = sqlite3.connect(r'D:/kursy/project/grsmu_diplom/db.sqlite3')

cur = conn.cursor()

## DB INSERT IP
# cur.execute("INSERT INTO proxie_proxie (ip) VALUES ('192.156.22:34');")
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
cur.execute("DELETE FROM proxie_proxie WHERE ip='192.156.22:34';")
conn.commit()
cur.execute("SELECT ip FROM proxie_proxie;")
result = cur.fetchall()
print(result)