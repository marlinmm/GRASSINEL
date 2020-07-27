import sys
from GEO450_GRASS_S1.support_functions import *

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
    """
    ...
    :return:
    """
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
    ...
    :return:
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


def import_shapefile(path_to_shape, overwrite_bool):
    """

    :param path_to_shape:
    :param overwrite_bool:
    :return:
    """
    ogrimport = Module("v.in.ogr")
    ogrimport(path_to_shape, overwrite=overwrite_bool)


def test():
    acitve_vector_data_list = []
    # show_active_data = Module("g.list")
    # show_active_data(type="vector", flags="m")
    # tmp = extract_files_to_list(Paths.send_down_path, datatype=".tif")
    # print(tmp)
    print(len("S1A__IW___D_20200530T052558_VV_NR_Orb_ML_TF_TC_dB.tif"))


def sen_download(start_time, end_time, sort_by):
    """
    ...
    :param start_time:
    :param end_time:
    :param sort_by:
    :return:
    """
    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
        ### Linux folder ###
        settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        output=Paths.send_down_path,
        ### Windows folder ###
        # settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        # output="F:/GEO450_GRASS/Data/sentinel/test_GEO450",
        map="jena_boundary@PERMANENT",
        area_relation="Contains",
        producttype="GRD",
        start=start_time,
        end=end_time,
        sort=sort_by,
        order="asc")


def sen_download_new(start_time, end_time, sort_by, relative_orbit_number):
    """
    ...
    :param start_time:
    :param end_time:
    :param sort_by:
    :param relative_orbit_number:
    :return:
    """
    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
        ### Linux folder ###
        settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        output=Paths.send_down_path,
        ### Windows folder ###
        # settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        # output="F:/GEO450_GRASS/Data/sentinel/test_GEO450",
        map="jena_boundary@PERMANENT",
        area_relation="Contains",
        producttype="GRD",
        start=start_time,
        end=end_time,
        sort=sort_by,
        order="desc",
        ### added capability for specific "relativeorbitnumber", needs changes to i.sentinel.download.py first!!! ###
        relativeorbitnumber=relative_orbit_number)


def pyroSAR_processing(start_time, target_resolution, target_CRS, terrain_flat_bool, remove_therm_noise_bool):
    """
    ...
    :param start_time:
    :param target_resolution:
    :param target_CRS:
    :param terrain_flat_bool:
    :param remove_therm_noise_bool:
    :return:
    """
    from datetime import datetime
    from pyroSAR.snap.util import geocode

    sentinel_file_list = extract_files_to_list(Paths.send_down_path, datatype=".zip")
    for l, file in enumerate(sentinel_file_list):
        geocode(infile=file, outdir=Paths.sen_processed_path, tr=target_resolution, t_srs=target_CRS,
               terrainFlattening=terrain_flat_bool, removeS1ThermalNoise=remove_therm_noise_bool)

        interval_time = datetime.now()
        print("file " + str(l+1) + " of " + str(len(sentinel_file_list)+1) + " processed in " + str(interval_time - start_time) + " Hr:min:sec")
    subset_path = subset_processed_data()
    subset_import(subset_path=subset_path, overwrite_bool=True)


def subset_import(subset_path, overwrite_bool):
    """
    imports the subsetted raster files into GRASS GIS, renames it into "rasterfile XX" and writes a text file for
    further processing (especially for the creation of a space time cube (see create_stc function below))
    :param subset_path:
    :param overwrite:
    :return:
    """
    file_list = extract_files_to_list(path_to_folder=subset_path, datatype=".tif")
    for i, tifs in enumerate(file_list):
        print(tifs)
        sensubsetlimport = Module("r.in.gdal")
        sensubsetlimport(
            input=tifs,
            output="rasterfile" + str(i),
            memory=300,
            offset=0,
            num_digits=0,
            overwrite=overwrite_bool)

    with open("/home/user/Desktop/GRASS Jena Workshop/sentinel-filelist.txt", "w") as f:
        i = -1
        for item in file_list:
            string = "__IW___"
            if item.__contains__(string):
                print(item.index(string))
                i = i + 1
                f.write("rasterfile" + str(i) + "|" + item[58:62] + "-" + item[62:64] + "-" + item[64:66] + "|" + item[74:76] + "\n")



def create_stc(overwrite_bool):
    """
    TODO: VISUALIZE STC VIA GUI ANIMATION TOOL !!!
    creates a space time cube for Sentinel time series analysis purposes
    :return:
    """
    create_stc = Module("t.create")
    create_stc(overwrite = overwrite_bool,
                output="stc",
                type="strds",
                temporaltype="absolute",
                semantictype="mean",
                title="stc",
                description="stc")

    register_stc = Module("t.register")
    register_stc(overwrite = overwrite_bool,
                 input="stc@PERMANENT",
                 type="raster",
                 file="/home/user/Desktop/GRASS Jena Workshop/sentinel-filelist.txt",
                 separator="pipe")

    info_stc = Module("t.info")
    info_stc(input="stc@PERMANENT",
                type="strds")
