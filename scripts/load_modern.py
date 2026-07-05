import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# https://py4e-data.dr-chuck.net/opengeo?q=Ann+Arbor%2C+MI
#serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('observatories.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Observatories (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
name TEXT NOT NULL UNIQUE, 
instruments TEXT, 
altitude INTEGER, 
type TEXT, 
lon REAL, 
lat REAL)
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("eso_data.json")
data = json.load(fh)
count = 0
num = input("Enter the number of records to retireve:")
if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(1)

for info in data:
    if count > 100 :
        print('Retrieved 100 locations, restart to retrieve more')
        break
        
    name = info[0]
    print(name)
    instruments = info[1]
    altitude = info[2]
    type_val = info[3]
    lon = info[4]
    lat = info[5]
    print(lon,lat)

    cur.execute("SELECT name FROM Observatories WHERE name= ?",(name,))
    if cur.fetchone() is not None:
        continue

    try:
        name = cur.fetchone()[0]
        print("Found in database", name)
        continue
    except:
        pass

    count = count + 1
    print(count)
        
    cur.execute('''INSERT INTO Observatories (name, instruments, altitude, type, lon, lat) 
    VALUES( ?, ?, ?, ?, ?, ? )''', 
    (name, instruments, altitude, type_val, lon, lat))

    conn.commit()
    
print("Run dump_modern.py to read the modern data from the database so you can vizualize it on a map.")
