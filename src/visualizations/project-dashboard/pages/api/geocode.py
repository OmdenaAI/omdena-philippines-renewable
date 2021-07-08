

# geocode and corect the DOE dataset using python3
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

doe_file = open("doe_powerstations_dataset.json")
ph_clustered_file = open("ph_clustered.json")

doe_data = json.load(doe_file)
ph_brgy = json.load(ph_clustered_file)

print("Starting Geoding Correction...")
print("==================================")


for data in doe_data:
  print(data["latitude"])

# close files

doe_file.close()
ph_clustered_file.close()
