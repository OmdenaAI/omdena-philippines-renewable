import json
  
# task 2 data
task2_data_file = open('./correlated_v1.json',)
task4_data_file = open("./task4_data.json")
  

# load datasets
task2_data = json.load(task2_data_file)
task4_data = json.load(task4_data_file)

opt_features = []

for x in task4_data:
    delta = {"type":"Feature",
    "geometry":{"type":"Point","coordinates":[x["Longitude"],x["Latitude"]]},
    "properties":{
        "SCORE": 0,
        "POP1": x["POP1"],
        "Longitude": x["Longitude"],
        "Latitude": x["Latitude"],
        "municipality": x["Municipalities"],
        "pvout_comp": x["PVOut_Comp"], 
        "pvout_wb": x["PVOut_WB"], 
        }
        }

    opt_features.append(delta)    


task2_data["features"] = opt_features;


print "==========================="
print "Task 2 data length:"
print(len(task2_data["features"]))
print "Task 4 data length:"
print(len(task4_data))
print "Optimization completed!"


# write json to file
with open('correlated_v2.json', 'w') as outfile:
    json.dump(task2_data, outfile)
  
