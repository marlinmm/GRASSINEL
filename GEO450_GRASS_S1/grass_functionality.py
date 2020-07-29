import sys
from GEO450_GRASS_S1.support_functions import *
from grass_session import Session, get_grass_gisbase
from grass_session import Session
import grass.script as gscript
import grass.script.setup as gsetup
from grass.pygrass.modules import Module


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
    # print(len("S1A__IW___D_20200530T052558_VV_NR_Orb_ML_TF_TC_dB.tif"))


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
        print("file " + str(l + 1) + " of " + str(len(sentinel_file_list) + 1) + " processed in " + str(
            interval_time - start_time) + " Hr:min:sec")
    subset_processed_data()


def subset_import(overwrite_bool, output, polarization_type):
    """
    TODO: UMKREMPELN VON DER FILE_LIST DAMIT DER DAS NACH TAG UND MONAT CHRONOLOGISCH SORTIERT!!!

    imports the subsetted raster files into GRASS GIS, renames it into "rasterfile XX" and writes a text file for
    further processing (especially for the creation of a space time cube (see create_stc function below))
    :param polarization_type:
    :param output:
    :param overwrite_bool:
    :param subset_path:
    :return:
    """

    for pol in polarization_type:
        file_list = extract_files_to_list(path_to_folder=Paths.subset_path, datatype=".tif")
        string = "IW___"
        cut_list = []
        for i in file_list:
            if i.__contains__(string):
                cut_list.append(i[i.index(string)+7:])
        cut_list.sort()

        sub_list = [j for j in file_list if pol in j]
        filelist_path = os.path.join(Paths.main_path, ("sentinel-filelist" + pol + ".txt"))
        for i, tifs in enumerate(sub_list):
            print(tifs)
            sensubsetlimport = Module("r.in.gdal")
            sensubsetlimport(input=tifs,
                             output=output + pol + str(i),
                             memory=500,
                             offset=0,
                             num_digits=0,
                             overwrite=overwrite_bool)

        with open(filelist_path, "w") as f:
            i = -1
            for item in cut_list:
                polarization = pol
                if item.__contains__(pol):
                    i = i + 1
                    f.write(output + pol + str(i) + "|" + item[:4] + "-" +
                            item[4:6] + "-" +
                            item[6:8] + " " +
                            item[9:11] + ":" +
                            item[11:13] + "|" +
                            item[16:18] + "\n")


def create_stc(overwrite_bool, output, polarization_type):
    """
    TODO: VISUALIZE STC VIA GUI ANIMATION TOOL WOULD BE NICE!!!
    creates and registers a space time cube for Sentinel time series analysis purposes and shows metadata information
    :param polarization_type:
    :param overwrite_bool:
    :param output:
    :return:
    """
    for pol in polarization_type:
        create_stc = Module("t.create")
        create_stc(overwrite=overwrite_bool,
                   output=output + pol,
                   type="strds",
                   temporaltype="absolute",
                   semantictype="mean",
                   title="stc",
                   description="stc")

        register_stc = Module("t.register")
        register_stc(overwrite=overwrite_bool,
                     input=output + pol,
                     type="raster",
                     file=os.path.join(Paths.main_path, ("sentinel-filelist" + pol + ".txt")),
                     separator="pipe")

        info_stc = Module("t.info")
        info_stc(input=output + pol, type="strds")


def t_rast_algebra(basename, expression):
    """
    TODO: NEEDS TO CHANGE BASENAME AND EXPRESSION FOR EVERY SINGLE CALCULATION!!! BECAUSE OVERWRITE IS NOT POSSIBLE!!!
    calculates user dependent raster functions on the space time cubes
    :param result_name:
    :param expression:
    :return:
    """
    raster_algebra = Module("t.rast.algebra")
    raster_algebra(flags='sng',
                   expression=expression,
                   basename=basename,
                   suffix="num",
                   nprocs=1)


def raster_report(overwrite_bool):
    """
    TODO: DOENST WORK YET!
    :return:
    """
    raster_report = Module("r.report")
    raster_report(overwrite=overwrite_bool,
                  map="product13_0@PERMANENT",
                  units="k",
                  null_value="*",
                  page_length=0,
                  page_width=79,
                  nsteps=255)
