import json 

#open crowded file 
with open('eso_data_old.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)
    new_list = []   

# separate each field 
for record in old_data:
    #print(record)
    name = record.get("name")
    print(name)
    instruments = record.get("instruments")
    #print(instruments)
    altitude = record.get("altitude")
    type_val = record.get("type")
    geo = record.get("geo_point_2d")
    if geo is not None:
        lon = geo.get("lon")
        lat = geo.get("lat")
    else:
        lon = 0.0
        lat = 0.0
    #print(lon, lat)
    
    record_list = [name, instruments, altitude, type_val, lon, lat]
    new_list.append(record_list)
    
# save it with neat 4 space indentations 
with open('eso_data.json', 'w', encoding='utf-8') as f:
    json.dump(new_list, f, indent=4, ensure_ascii=False)
    
print("Created 'eso_data.json' ! Open this new file to see it beautifully organized.")