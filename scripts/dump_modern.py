import sqlite3
import json
import codecs

conn = sqlite3.connect('observatories.sqlite')
cur = conn.cursor()

BASE_QUERY = 'SELECT id, name, instruments, altitude, type, lon, lat FROM Observatories WHERE type = "Modern Astronomical Observatory" AND instruments is NOT NULL'
# Separting each type using queries 
print("Processing Type 1: Radio")
f_radio = codecs.open('map_radio.js', 'w', "utf-8")
f_radio.write("radioData = [\n")
count_radio = 0 

print("Processing Type 2: Laser")
f_laser = codecs.open('map_laser.js', 'w', "utf-8")
f_laser.write("laserData = [\n")
count_laser = 0 

print("Processing Type 3: Infrared")
f_infrared = codecs.open('map_infrared.js', 'w', "utf-8")
f_infrared.write("infraredData = [\n")
count_infrared = 0 

print("Processing Type 4: Infrared Radio")
f_infrared_radio = codecs.open('map_IR_radio.js', 'w', "utf-8")
f_infrared_radio.write("IR_radioData = [\n")
count_infrared_radio = 0 

print("Processing Type 5: Laser Radio")
f_laser_radio = codecs.open('map_laser_radio.js', 'w', "utf-8")
f_laser_radio.write("laser_radioData = [\n")
count_laser_radio = 0 

print("Processing Type 6: Infrared Laser")
f_infrared_laser = codecs.open('map_infrared_laser.js', 'w', "utf-8")
f_infrared_laser.write("IR_laserData = [\n")
count_infrared_laser = 0 

print("scanning all records together...")
cur.execute(BASE_QUERY)
##(8,'Daeduk Radio Astronomical Observatory R Taejeon','Radio',120,'Modern Astronomical Observatory', 127.371666666667, 36.3983333333333)
#  0                         1                              2      3                   4                         5       6
## loop starts here
for row in cur :
    print(row)
    id_val = row[0]
    name = row[1]
    instruments = row[2]
    inst = row[2].lower()
    altitude = row[3]
    if altitude is None:
        altitude = 0
    type_val = row[4]
    lon = row[5]
    lat = row[6]
    
    name = name.replace("'", "")
    name = name.replace(",", "")
    name= name.replace("/", "")

    output = "['"+ name +"', "+str(lat)+", "+ str(lon) +"]"
   
    # counting total records for specific instrument
    if "radio" in inst and "laser" not in inst and "infrared" not in inst : 
        if count_radio > 0 : f_radio.write(",\n") 
        f_radio.write(output) 
        count_radio = count_radio + 1 

    if "laser" in inst and "infrared" not in inst and "radio" not in inst : 
        if count_laser > 0 : f_laser.write(",\n") 
        f_laser.write(output) 
        count_laser = count_laser + 1 

    if "infrared" in inst and "radio" not in inst and "laser" not in inst : 
        if count_infrared > 0 : f_infrared.write(",\n") 
        f_infrared.write(output) 
        count_infrared = count_infrared + 1 

    if "infrared" in inst and "radio" in inst and "laser" not in inst : 
        if count_infrared_radio > 0 : f_infrared_radio.write(",\n") 
        f_infrared_radio.write(output) 
        count_infrared_radio = count_infrared_radio + 1 

    if "laser" in inst and "radio" in inst and "infrared" not in inst: 
        if count_laser_radio > 0 : f_laser_radio.write(",\n") 
        f_laser_radio.write(output) 
        count_laser_radio = count_laser_radio + 1 

    if "infrared" in inst and "laser" in inst and "radio" not in inst : 
        if count_infrared_laser > 0 : f_infrared_laser.write(",\n") 
        f_infrared_laser.write(output) 
        count_infrared_laser = count_infrared_laser + 1 

# rewrite the .js files
##closing statement 

f_radio.write("\n];\n")
f_radio.close()

f_laser.write("\n];\n")
f_laser.close()

f_infrared.write("\n];\n")
f_infrared.close()

f_infrared_radio.write("\n];\n")
f_infrared_radio.close()

f_laser_radio.write("\n];\n")
f_laser_radio.close()

f_infrared_laser.write("\n];\n")
f_infrared_laser.close()

## print count
print("\n___ Summary Results ___")
print("Instruments records written to map_radio.js", count_radio)
print("Instruments records written to map_laser.js", count_laser)
print("Instruments records written to map_infrared.js", count_infrared)
print("Instruments records written to map_infrared_radio.js", count_infrared_radio)
print("Instruments records written to map_laser_radio.js", count_laser_radio)
print("Instruments records written to map_infrared_laser.js", count_infrared_laser)

cur.close()
conn.close()
print("Open map.html to view the data in a browser")

