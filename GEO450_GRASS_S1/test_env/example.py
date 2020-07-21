#!/usr/bin/env python


import os

from GEO450_GRASS_S1.test_env.python_setup import GRASSBIN_import
grassbin = GRASSBIN_import()
os.environ['GRASSBIN'] = grassbin

from grass_session import Session
# import grass python libraries
from grass.pygrass.modules import Module

# simple example for pyGRASS usage: raster processing via modules approach
# Windows path
# gisdb = 'F:/GEO450_GRASS/test_python'
# Linux path
gisdb = '/home/user/grassdata'
location = 'test3'
mapset = 'PERMANENT'

## IMPORT AND INSTALL SENTINELSAT FIRST !!! ##

# set some common environmental variables, like for raster compression settings:
with Session(gisdb=gisdb, location=location, create_opts='EPSG:32632'):
    #def ogrimport():
    ## function body to be added here ##


    #### RUN THIS SHIT BEFORE RUNNING SENTINELDOWNLOAD!!!!!!
    # ogrimport = Module("v.in.ogr")
    # ogrimport("/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_boundary.gpkg")

    #print(v.info(map='jena_boundary'))

    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
                ### Linux folder ###
                settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
                output="/home/user/Desktop/GRASS Jena Workshop/geodata/sentinel/Sentinel_Download",
                ### Windows folder ###
                # settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
                # output="F:/GEO450_GRASS/Data/sentinel/test_GEO450",
                map="jena_boundary@PERMANENT",
                area_relation="Intersects",
                producttype="GRD",
                start="2020-06-02",
                end="2020-06-10",
                sort="ingestiondate",
                order="asc")

