import os
import sys
os.environ["GISBASE"] = "/usr/lib/grass79/"
sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))
sys.path.insert(0, os.path.join(os.environ['GISBASE'], 'etc', 'python'))

##################################################################################
# general GRASS setup
# Windows
grass7bin_win = r'C:/OSGeo4W64/bin/grass79.bat'
# Linux
grass7bin_lin = 'grass79'

if sys.platform.startswith('linux'):
    # we assume that the GRASS GIS start script is available and in the PATH
    # query GRASS 7 itself for its GISBASE
    grass7bin = grass7bin_lin
elif sys.platform.startswith('win'):
    grass7bin = grass7bin_win

grassbin = grass7bin
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
### Linux path <- add path here for each Linux user and do not overwrite!
gisdb = '/home/user/grassdata'

### Windows path <- add path here for each Windows user and do not overwrite!
# gisdb = 'F:/GEO450_GRASS/test_python'
location = 'test4'
mapset = 'PERMANENT'
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
# nprint('Current GRASS GIS 7 environment:')
# print(gscript.gisenv())
##################################################################################