import sys
from GEO450_GRASS_S1.user_data import *

from grass_session import Session, get_grass_gisbase
from grass_session import Session
import grass.script as gscript
import grass.script.setup as gsetup

from grass.pygrass.modules import Module
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import temporal as t
from grass.pygrass.modules.shortcuts import display as d


def GRASSBIN_import():
    # general GRASS setup
    # input your Windows path
    grass7bin_win = r'C:/OSGeo4W64/bin/grass79.bat'
    # set your Linux grass version
    grass7bin_lin = GRASS_data.grass_version

    if sys.platform.startswith('linux'):
        # we assume that the GRASS GIS start script is available and in the PATH
        # query GRASS 7 itself for its GISBASE
        grass7bin = grass7bin_lin
    elif sys.platform.startswith('win'):
        grass7bin = grass7bin_win
    print(grass7bin)
    return grass7bin


def grass_setup():
    """
    ....
    """

    location_name = GRASS_data.location_name
    crs = GRASS_data.crs

    grassbin = GRASSBIN_import()
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
                 location=GRASS_data.location_name,
                 create_opts='EPSG:' + crs) as session:
        pass
    ##################################################################################
    # launch session
    gsetup.init(gisbase, gisdb, location_name, mapset)
    print(f"Current GRASS GIS 7 environment: {gscript.gisenv()}")


def import_shapefile():
    ogrimport = Module("v.in.ogr")
    #ogrimport("/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_boundary.gpkg")
    #ogrimport("/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_rivers.gpkg")


def test():
    acitve_vector_data_list = []
    show_active_data = Module("g.list")
    show_active_data(type="vector", flags="m")
    #for elem in

def sen_download():
    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
        ### Linux folder ###
        settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        output=Paths.send_down_path,
        ### Windows folder ###
        # settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        # output="F:/GEO450_GRASS/Data/sentinel/test_GEO450",
        map="jena_boundary@PERMANENT",
        area_relation="Intersects",
        producttype="GRD",
        start="2020-06-02",
        end="2020-06-30",
        sort="ingestiondate",
        order="asc")
