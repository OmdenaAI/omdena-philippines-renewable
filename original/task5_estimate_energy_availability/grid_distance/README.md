# Grid distance
The goal of this subtask is to figure out the distance from the electrical grid in Nigeria to any point in Nigeria. This is potentially useful in 2 different ways: people living further away from the electrical grid might have a greater demand for solar panels, as it is not easy to provide electricity for them in any other way, and it might be financially beneficial to invest in solar panels further away from the electrical grid, as in the near future connection to the grid might become viable.

## Scripts
### electrical_grid.py
This script downloads and rasterizes the transmission network shapefiles from the World Bank. Note that the worldpop's estimated spatial distribution of the population of Nigeria in 2020 is required as a template to rasterize the electrical grid shapefiles from the World Bank.

### dist.py
This script calculates the distances to the electrical grid. It's a very naive approach right now; it starts by loading the worldpop tif of Nigeria (that should be located in the directory ../data/nga_ppp_2020.tif) and the electrical grid mapped by Development Seed, then for every pixel in the worldpop tif, it calculates the distance to nearby pixels in the electrical grid and saves the shortest of them.

### convert.py
This script converts the (current) NumPy array of distances to a tif.

### main.py
A script to produce the desired results of this subtask, using the previously mentioned scripts.

## Data
### World Bank Group
Nigeria Electricity Transmission Network. [Link](https://datacatalog.worldbank.org/dataset/nigeria-electricity-transmission-network).

### Development Seed
The electrical grid recognized through ML. [Link](https://datacatalog.worldbank.org/dataset/nigeria-high-resolution-high-voltage-grid-map-based-machine-learning).
