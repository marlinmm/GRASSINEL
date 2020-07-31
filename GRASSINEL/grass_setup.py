import sys
from GRASSINEL.support_functions import *
from GRASSINEL.user_data import *
from grass_session import get_grass_gisbase
from grass_session import Session
import grass.script as gscript
import grass.script.setup as gsetup

def GRASSBIN_import():
    """
    this function checks, what kind of OS is run and returns the corresponding grass7bin location
    return: grass7bin: string
        location of grass7bin
    """
    # general GRASS setup
    # input your Windows path
    grass7bin_win = r'C:/OSGeo4W64/bin/grass79.bat'
    # set your Linux grass version
    grass7bin_lin = GrassData.grass_version

    if sys.platform.startswith('linux'):
        # we assume that the GRASS GIS start script is available and in the PATH
        # query GRASS 7 itself for its GISBASE
        grass7bin = grass7bin_lin
    elif sys.platform.startswith('win'):
        grass7bin = grass7bin_win
    return grass7bin


def grass_setup():
    """
    this function initializes the GRASS session and creates the mapset with the user-specified variables
    """
    user_data()
    location_name = GrassData.location_name
    crs = GrassData.crs

    grassbin = GRASSBIN_import()
    if grassbin == "grass7bin_win":
        print("You're using Windows, this module most likely will not work properly, please use a linux-based OS!!!")
    os.environ['GRASSBIN'] = grassbin
    gisbase = get_grass_gisbase()
    os.environ['GISBASE'] = gisbase
    sys.path.append(os.path.join(os.environ['GISBASE'], 'bin'))
    sys.path.append(os.path.join(os.environ['GISBASE'], 'lib'))
    sys.path.append(os.path.join(os.environ['GISBASE'], 'scripts'))
    sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))

    # set folder to proj_lib:
    os.environ['PROJ_LIB'] = '/usr/share/proj'

    gisdb = Paths.grass_path
    mapset = "PERMANENT"
    ##################################################################################
    # open a GRASS session and create the mapset if it does not yet exist
    with Session(gisdb=gisdb,
                 location=GrassData.location_name,
                 create_opts='EPSG:' + crs):
        pass
    ##################################################################################
    # launch session
    gsetup.init(gisbase, gisdb, location_name, mapset)
    print(f"Current GRASS GIS 7 environment: {gscript.gisenv()}")
