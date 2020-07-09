import os
import sys
os.environ["GISBASE"] = "/usr/lib/grass79/"
sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))
sys.path.insert(0, os.path.join(os.environ['GISBASE'], 'etc', 'python'))

##################################################################################
# general GRASS setup
grassbin = "grass79"
os.environ['GRASSBIN'] = grassbin

from grass_session import Session, get_grass_gisbase

gisbase = get_grass_gisbase()

os.environ['GISBASE'] = gisbase
sys.path.append(os.path.join(os.environ['GISBASE'], 'bin'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'lib'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'scripts'))
sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))

# set folder to proj_lib:
os.environ['PROJ_LIB'] = '/usr/share/proj'

# to add grass to path permanently, open "bashrc" using command: vim bash
import grass.script as gscript
import grass.script.setup as gsetup

##################################################################################
# user-defined settings
gisdb = '/home/user/grassdata'
location = 'test1'
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
