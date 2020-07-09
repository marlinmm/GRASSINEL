#!/usr/bin/env python

import sentinelsat
from grass_session import Session
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
import os

# simple example for pyGRASS usage: raster processing via modules approach
gisdb = '/home/user/grassdata'
location = 'test1'
mapset = 'user'

## IMPORT AND INSTALL SENTINELSAT FIRST !!! ##

# set some common environmental variables, like for raster compression settings:
with Session(gisdb=gisdb, location=location, create_opts='EPSG:32632'):
    #def ogrimport():
    ## function body to be added here ##
    # ogrimport = Module("v.in.ogr")
    # ogrimport("/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_rivers.gpkg")
    # print(gcore.run_command())
    # print(v.info(map='jena_rivers'))

    sentineldownload = Module("i.sentinel.download")
    sentineldownload(settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
                output="/home/user/Desktop/GRASS Jena Workshop/geodata/sentinel/Sentinel_Download",
                map="jena_boundary@PERMANENT",
                area_relation="Intersects",
                producttype="GRD",
                start="2020-06-02",
                end="2020-06-10",
                sort="ingestiondate",
                order="asc")

