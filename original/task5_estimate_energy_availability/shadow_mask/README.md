# Shadow mask
The goal of this subtask is to find the areas in Nigeria that are covered with shadows. Naturally, some areas will be covered with shadows more often than others throughout a year, which therefore makes them less efficient for solar panels.

## Scripts
### srtm.py
This script downloads the necessary SRTM (version 4) files to cover all of Nigeria and merges them. 

### shadow.py
This script calculates shadows over Nigeria given some position of the sun.

### solar.py
This script calculates the position of the sun over mid-Nigeria given some date and time.

### main.py
A script to produce the desired results of this subtask, using the previous mentioned scripts.

## Data
### SRTM version 4
Cleaned radar images obtained by the Shuttle Radar Topography Mission (SRTM). [Link](http://srtm.csi.cgiar.org/).
