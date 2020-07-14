#!/usr/bin/env python


import os

from GEO450_GRASS_S1.python_setup import GRASSBIN_import
grassbin = GRASSBIN_import()
os.environ['GRASSBIN'] = grassbin

from grass_session import Session
import sentinelsat
from grass.script import core as gcore
import grass.script as gscript
import grass.script.setup as gsetup
# import grass python libraries
from grass.pygrass.modules import Module
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import temporal as t
from grass.pygrass.modules.shortcuts import display as d


# simple example for pyGRASS usage: raster processing via modules approach
# Windows path
# gisdb = 'F:/GEO450_GRASS/test_python'
# Linux path
def new_grasssession():
    gisdb = '/home/user/grassdata'
    location = 'test3'
    mapset = 'PERMANENT'

## IMPORT AND INSTALL SENTINELSAT FIRST !!! ##

# set some common environmental variables, like for raster compression settings:
with Session(gisdb=gisdb, location=location, create_opts='EPSG:32632'):

    ## function body to be added here ##


    #### RUN THIS SHIT BEFORE RUNNING SENTINELDOWNLOAD!!!!!!
    def ogrimport():
        ogrimport = Module("v.in.ogr")
        ogrimport("/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_boundary.gpkg")

    #print(v.info(map='jena_boundary'))

    def sentineldownload():
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

