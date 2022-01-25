import json

print("Cleaning correlated data...")

data_file = open("./correlated_v2.json")
data_loaded = json.load(data_file)

# coord simplifier
def round_floats(o):
    if isinstance(o, float):
        return round(o, 6)
    if isinstance(o, dict):
        return {k: round_floats(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [round_floats(x) for x in o]
    return o

# write to file
def writeTofile(file_data):
    print("File written successfully!")
    with open('crv2.json', 'w') as outfile:
        data = json.dumps(file_data,separators=(',', ':'))
        outfile.write(data)    

outData = {"type":"FeatureCollection","features":[]}

for i, x in enumerate(data_loaded["features"]):
    if x["geometry"]:
        new_geometry = round_floats(x["geometry"])
        new_properties = round_floats(x["properties"])
        try:
            outData["features"].append({"id":i,"type":"Feature","geometry":new_geometry,"properties": new_properties})
            print(i)
        except:
            print("ERROR ===> ROW")    
    else:
        print("ERROR ===> SEGMENT")         

writeTofile(outData)
print("karagatan patrol cleanup complete. [100%]")