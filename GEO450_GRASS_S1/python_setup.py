import os
import sys

##################################################################################
# general GRASS setup
grassbin = 'grass78'
os.environ['GRASSBIN'] = grassbin

from grass_session import Session, get_grass_gisbase

gisbase = get_grass_gisbase()

os.environ['GISBASE'] = gisbase
sys.path.append(os.path.join(os.environ['GISBASE'], 'bin'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'lib'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'scripts'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))

os.environ['PROJ_LIB'] = 'C:\\OSGeo4W64\\share\\proj'

import grass.script as gscript
import grass.script.setup as gsetup

##################################################################################
# user-defined settings
gisdb = 'E:\\DATA\\test\\GRASS'
location = 'Spain_Donana'
mapset = 'PERMANENT'
##################################################################################
# open a GRASS session and create the mapset if it does not yet exist
with Session(gisdb=gisdb,
             location=location,
             create_opts='EPSG:32629') as session:
    pass
##################################################################################
# launch session
gsetup.init(gisbase, gisdb, location, mapset)
print('Current GRASS GIS 7 environment:')
print(gscript.gisenv())
##################################################################################
