import os
import sys
# os.environ["GISBASE"] = "/usr/lib/grass79/" # Linux
# os.environ["GISBASE"] = "C:/OSGeo4W64/apps/grass/grass79/" # Windows
# sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))
# sys.path.insert(0, os.path.join(os.environ['GISBASE'], 'etc', 'python'))

##################################################################################
# general GRASS setup
grassbin = r'C:/OSGeo4W64/bin/grass79.bat'
os.environ['GRASSBIN'] = grassbin

from grass_session import Session, get_grass_gisbase

gisbase = get_grass_gisbase()

os.environ['GISBASE'] = gisbase
sys.path.append(os.path.join(os.environ['GISBASE'], 'bin'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'lib'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'scripts'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))

os.environ['PROJ_LIB'] = "C:/OSGeo4W64/share/proj"

import grass.script as gscript
import grass.script.setup as gsetup

##################################################################################
# user-defined settings
gisdb = 'F:/GEO450_GRASS/test_python/'
location = 'test_1'
mapset = 'user1'
##################################################################################
# open a GRASS session and create the mapset if it does not yet exist
with Session(gisdb=gisdb,
             location=location,
             mapset=mapset,
             create_opts='EPSG:25832') as session:
    pass
##################################################################################
# launch session
gsetup.init(gisbase, gisdb, location, mapset)
print('Current GRASS GIS 7 environment:')
print(gscript.gisenv())
##################################################################################
