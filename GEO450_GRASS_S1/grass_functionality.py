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


def import_shapefile(path_to_shape, overwrite_bool):
    ogrimport = Module("v.in.ogr")
    ogrimport(path_to_shape, overwrite=overwrite_bool)


def test():
    acitve_vector_data_list = []
    # show_active_data = Module("g.list")
    # show_active_data(type="vector", flags="m")
    tmp = extract_files_to_list(Paths.send_down_path, datatype=".tif")
    print(tmp)


def sen_download(start_time, end_time, sort_by):
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


def extract_files_to_list(path_to_folder, datatype):
    """
    finds all .tif-files in the corresponding directory
    :return:
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(datatype):
            new_list.append(os.path.join(path_to_folder, filename))
        else:
            continue
    return new_list


def import_polygons():
    """
    imports the 3x3km polygons of the DWD weather stations
    :return:
    """
    import fiona
    shape_list = []
    active_shapefile = fiona.open(Paths.boundary_path, "r")
    for i in range(0,len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
        shape_list.append(shapes)
    return shape_list


def pyroSAR_processing(target_resolution, target_CRS, terrain_flat_bool, remove_therm_noise_bool):
    from pyroSAR.snap.util import geocode

    sentinel_file_list = extract_files_to_list(Paths.send_down_path, datatype=".zip")
    for file in sentinel_file_list:
        geocode(infile=file, outdir=Paths.sen_processed_path, tr=target_resolution, t_srs=target_CRS,
                terrainFlattening=terrain_flat_bool, removeS1ThermalNoise=remove_therm_noise_bool)
    subset_processed_data()


def subset_processed_data():
    import rasterio as rio
    import rasterio.mask
    import numpy as np
    ### install BanDiTS using: python3.6 -m pip install git+https://github.com/marlinmm/BanDiTS.git ###
    from BanDiTS.export_arr import functions_out_array
    processed_file_list = extract_files_to_list(Paths.sen_processed_path, datatype=".tif")
    shapefile = import_polygons()
    for k, tifs in enumerate(processed_file_list):
        src1 = rio.open(processed_file_list[k])
        out_image1, out_transform1 = rio.mask.mask(src1, [shapefile[0][0]], all_touched=1, crop=True,
                                                   nodata=np.nan)
        ras_meta1 = src1.profile
        ras_meta1.update({"driver": "GTiff",
                         "height": out_image1.shape[1],
                         "width": out_image1.shape[2],
                         "transform": out_transform1,
                         "nodata": -9999})
        functions_out_array(outname=processed_file_list[k][:-4] + "_subset.tif", arr=out_image1,
                            input_file=processed_file_list[k], dtype=np.float32, ras_meta1=ras_meta1)

