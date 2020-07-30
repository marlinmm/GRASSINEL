# GEO450_GRASS_S1
University Project (FSU Jena) by Jonas Ziemer, Marlin M. Mueller and Patrick Fischer

This tool combines [pyroSAR](https://github.com/johntruckenbrodt/pyroSAR) Sentinel-1 preprocessing capabilites with 
[GRASS GIS](grass.osgeo.org) functionality for Sentinel satellite imagery. 

It allows for automatic downloading of user-defined Sentinel-1 scenes, pre-processing, subsetting and multitemporal
operations. Data is handled in GRASS internal formats and all available GRASS operations can be applied

####Functionality Overview:
* Automatic Setup of GRASS environment
* Automatic download of Sentinel-1 data using the GRASS addon i.sentinel.download
* Pre-processing of downloaded Sentinel-1 using pyroSAR functionality ([ESA SNAP](http://step.esa.int/main/download/snap-download/)
 is required for the processing, see [here](https://pyrosar.readthedocs.io/en/latest/?badge=latest))
* Automatic subetting of satellite data to specified region of interest
* GRASS functionalty:
    * Creation of space time raster datasets (STRDS) in GRASS
    * Different mutitemporal operations in GRASS
* Future functionality:
    * pyWPS implementation

_Developed in Python 3.6, currently only supported on linux-based OS_

# Installation
In case you have git installed you can install the package as follows:

    pip install git+https://github.com/marlinmm/GEO450_GRASS_S1.git

