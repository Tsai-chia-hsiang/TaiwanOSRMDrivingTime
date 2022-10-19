# OpenStreetMap OSRM API To get driving time

This is a project about using python ```routingpy.osrm``` API 
to get driving distance & driving time from __OpenStreetMap__ data by using osrm API.

In this project, I use osrm to get the driving time and distance about the pairs of Taiwanese toursit attractions. 

The class ```Router()``` in file ```calculateDist.py``` is customized for our file structure.

The mainly useage of the notebook ```script.ipynb``` is for unit execution.

### Environment
python package:
- routingpy
  
  **Note: need ```GDAL``` &```geopandas```** package and these 2 may be a little bit hard to setup.
- pandas 
- numpy 
