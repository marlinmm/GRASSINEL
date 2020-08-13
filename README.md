# GRASSINEL
University Project (FSU Jena) by Jonas Ziemer, Marlin M. Mueller and Patrick Fischer

This tool combines [pyroSAR](https://github.com/johntruckenbrodt/pyroSAR) Sentinel-1 preprocessing capabilites with 
[GRASS GIS](grass.osgeo.org) functionality for Sentinel satellite imagery. 

It allows for automatic downloading of user-defined Sentinel-1 scenes, pre-processing, subsetting and multitemporal
operations. Data is handled in GRASS internal formats and all available GRASS operations can be applied

#### Functionality Overview:
* Automatic Setup of GRASS environment
* Automatic download of Sentinel-1 data using the GRASS addon i.sentinel.download
* Pre-processing of downloaded Sentinel-1 using pyroSAR functionality ([ESA SNAP](http://step.esa.int/main/download/snap-download/)
 is required for the processing, see [here](https://pyrosar.readthedocs.io/en/latest/?badge=latest))
* Automatic subsetting of satellite data to specified region of interest
* GRASS functionality:
    * Creation of space time raster datasets (STRDS) in GRASS
    * Different multitemporal operations in GRASS
* Future functionality:
    * pyWPS implementation

_Developed in Python 3.6, currently only supported on linux-based OS_

# Installation
In case you have git installed you can install the package as follows:

    pip install git+https://github.com/marlinmm/GRASSINEL.git

# Examples
Example of created timeseries processed using pyroSAR and created using GRASS GIS time series functionality
![S1_time_series_20m](GRASSINEL/preview_files/S1_timeseries_20m_example.gif) 

 +-------------------- Space Time Raster Dataset -----------------------------+
 |                                                                            |
 +-------------------- Basic information -------------------------------------+
 | Id: ........................ stcubeVH@PERMANENT
 | Name: ...................... stcubeVH
 | Mapset: .................... PERMANENT
 | Creator: ................... user
 | Temporal type: ............. absolute
 | Creation time: ............. 2020-08-13 16:06:33.953310
 | Modification time:.......... 2020-08-13 16:06:34.904234
 | Semantic type:.............. mean
 +-------------------- Absolute time -----------------------------------------+
 | Start time:................. 2020-06-01 00:00:00
 | End time:................... 2020-06-07 00:00:00
 | Granularity:................ 1 day
 | Temporal type of maps:...... point
 +-------------------- Spatial extent ----------------------------------------+
 | North:...................... 5651724.983936
 | South:...................... 5636914.26438
 | East:.. .................... 687777.63231
 | West:....................... 675476.252098
 | Top:........................ 0.0
 | Bottom:..................... 0.0
 +-------------------- Metadata information ----------------------------------+
 | Raster register table:...... raster_map_register_287261ed0b5c4ae48ff4fba1689ee2bd
 | North-South resolution min:. 50.0
 | North-South resolution max:. 50.0
 | East-west resolution min:... 50.0
 | East-west resolution max:... 50.0
 | Minimum value min:.......... -24.231297
 | Minimum value max:.......... -21.883429
 | Maximum value min:.......... 5.870026
 | Maximum value max:.......... 8.514816
 | Aggregation type:........... None
 | Number of registered bands:. 1
 | Number of registered maps:.. 4
 |
 | Title:
 | stc
 | Description:
 | stc
 | Command history:
 | # 2020-08-13 16:06:33 
 | t.create type="strds" temporaltype="absolute"
 |     semantictype="mean" title="stc" description="stc" output="stcubeVH" --o
 | # 2020-08-13 16:06:34 
 | t.register input="stcubeVH" type="raster"
 |     file="/home/user/Desktop/GRASSINEL_dir/sentinel-filelistVH.txt"
 |     separator="pipe" --o
 | 
 +----------------------------------------------------------------------------+

![S1_time_series_50m](GRASSINEL/preview_files/S1_timeseries_50m_example.gif) 
