from GRASSINEL.support_functions import *
from grass.pygrass.modules import Module


def import_shapefile(path_to_shape, overwrite_bool):
    """
    imports the boundary of the area of investigation
    :param path_to_shape: string
        Path to folder, where the shapefile is
    :param overwrite_bool: bool
        Option of True or False, but True is strongly recommended!
    :return:
    """
    ogrimport = Module("v.in.ogr")
    ogrimport(path_to_shape, overwrite=overwrite_bool)


def sen_download(start_time, end_time, sort_by):
    """
    this function takes some parameters and downloads Sentinel-1 data using GRASS functions accordingly
    :param start_time: string
        start date for the Sentinel-1 data download search
    :param end_time: string
        end date for the Sentinel-1 data download search
    :param sort_by: string
        variable to sort Sentinel-1 data by
    """
    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
        settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        output=Paths.sen_down_path,
        map="jena_boundary@PERMANENT",
        area_relation="Contains",
        producttype="GRD",
        start=start_time,
        end=end_time,
        sort=sort_by,
        order="asc")


def sen_download_extended(start_time, end_time, sort_by, relative_orbit_number):
    """
    this function takes some parameters and downloads Sentinel-1 data using GRASS functions accordingly

    !!! this function needs changes to i.sentinel.download first to work, changes are requested to official OSGEO
    grass-addons repo !!!

    :param start_time: string
        start date for the Sentinel-1 data download search
    :param end_time: string
        end date for the Sentinel-1 data download search
    :param sort_by: string
        variable to sort Sentinel-1 data by
    :param relative_orbit_number: int
        this variable lets user specifically choose one relative orbit number to always receive the same orbit files
    """
    sentineldownload = Module("i.sentinel.download")
    sentineldownload(
        settings="/home/user/Desktop/GRASS Jena Workshop/settings.txt",
        output=Paths.sen_down_path,
        map="jena_boundary@PERMANENT",
        area_relation="Contains",
        producttype="GRD",
        start=start_time,
        end=end_time,
        sort=sort_by,
        order="desc",
        ### added capability for specific "relativeorbitnumber", needs changes to i.sentinel.download.py first!!! ###
        relativeorbitnumber=relative_orbit_number)


def subset_import(overwrite_bool, output, polarization_type):
    """
    imports the subsetted raster files into GRASS GIS, renames it into "rasterfile XX" and writes a text file for
    further processing (especially for the creation of a space time cube (see create_stc function below))
    :param overwrite_bool: bool
        Option of True or False, but True is strongly recommended!
    :param output: string
        Output name for every single rasterfile of the space-time-cube
    :param polarization_type: list
        Choice between cross-polarization (VH) and/or co-polarization (VV) -> example: ["VH", "VV"]
    """
    for pol in polarization_type:
        file_list = extract_files_to_list(path_to_folder=Paths.subset_path, datatype=".tif")
        string = "IW___"
        cut_list = []
        for i in file_list:
            if i.__contains__(string):
                cut_list.append(i[i.index(string) + 7:])
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
                            # For minute resolution
                            #item[9:11] + ":" +
                            #item[11:13] +
                            "|" +
                            item[16:18] + "\n")


def create_stc(overwrite_bool, output, polarization_type, stc_info_bool, stc_statistics_bool):
    """
    creates and registers a space time cube for Sentinel time series analysis purposes and shows metadata information
    :param overwrite_bool: bool
        Option of True or False, but True is strongly recommended!
    :param output: string
        Name of the space-time-cube to create & analyze in GRASS GIS
    :param polarization_type: list
        Choice between cross-polarization (VH) and/or co-polarization (VV) -> example: ["VH", "VV"]
    :param stc_info_bool: bool
        Option of True or False, returns temporal and spatial informations about the stc
    :param stc_statistics_bool: bool
        Option of True or False, returns temporal and spatial statistics about every single raster scene of the stc
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

        if stc_info_bool:
            info_stc = Module("t.info")
            info_stc(input=output + pol, type="strds")

    if stc_statistics_bool:
        for pol in polarization_type:
            stc_statistics = Module("t.rast.univar")
            stc_statistics(flags='er',
                    overwrite=True,
                    input=output + pol,
                    separator="pipe")


def visualize_stc(output, polarization_type, stc_animation_bool, stc_timeline_bool):
    """
    visualizes the input space-time-cubes according to user-dependent purposes
    :param output: string
        Name of the space-time-cube to vizualize in GRASS GIS
    :param polarization_type: list
        Choice between cross-polarization (VH) and/or co-polarization (VV) -> example: ["VH", "VV"]
    :param stc_animation_bool: bool
        Option of True or False, animates temporally the space-time-cube with GRASS Animation Tool
    :param stc_timeline_bool: bool
        Option of True or False, returns a timeline plot with all downloaded dates with GRASS Timeline Tool
    :return:
    """
    for pol in polarization_type:
        if stc_animation_bool:
            if len(polarization_type) > 1:
                stc_animation = Module("g.gui.animation")
                print("----------------- " + str(polarization_type[0]) + " Time Series Animation" + " -----------------")
                stc_animation(strds=(output + polarization_type[0]))
                print("----------------- " + str(polarization_type[1]) + " Time Series Animation" + " -----------------")
                stc_animation(strds=(output + polarization_type[1]))
            else:
                stc_animation = Module("g.gui.animation")
                print("----------------- " + str(pol) + " Time Series Animation" + " -----------------")
                stc_animation(strds=output+pol)

        if stc_timeline_bool:
            print("----------------------- " + "Timeline Plot" + " ----------------------")
            if len(polarization_type) > 1:
                stc_timeline = Module("g.gui.timeline")
                stc_timeline(inputs=(output + polarization_type[0], output + polarization_type[1]))
            else:
                stc_timeline = Module("g.gui.timeline")
                stc_timeline(inputs=(output + pol))


def raster_algebra(basename, layername, expression, overwrite_bool):
    """
    calculates user-dependent raster-algebra functions on the imported space-time-cube
    :param basename: string
        Output tif-name
    :param layername: string
        Name of the formula result, e.g. "result"
    :param expression: string
        mathematic formula the raster calculation is based on
    :param overwrite_bool: bool
        Option of True or False, but True is strongly recommended!
    :return:
    """
    g_list_output(overwrite_bool)
    t_list_output(overwrite_bool)
    acive_strds = open(os.path.join(Paths.main_path, "t_list_output"))
    strds_list = acive_strds.readlines()
    active_raster = open(os.path.join(Paths.main_path, "g_list_output"))
    raster = active_raster.read()
    raster_list = list(raster.split(sep=","))
    for raster in raster_list:
        if basename in raster:
            g_remove(raster_name=raster)
    for strds in strds_list:
        if layername in strds:
            t_remove(strds_name=strds)

    raster_algebra = Module("t.rast.algebra")
    raster_algebra(flags='sng',
                   expression=layername + expression,
                   basename=basename,
                   suffix="num",
                   nprocs=4)


def rvi_mapcalc(layername, overwrite_bool):
    """
    calculates the radar vegetation index for all file of the space-time-cube
    :param layername: string
        Name of the output layer
    :param overwrite_bool: bool
        Option of True or False, but True is strongly recommended!
    :return:
    """
    VH = open(os.path.join(Paths.main_path, "sentinel-filelistVH.txt"))
    new_list = VH.readlines()
    file_VH_list = []
    file_VV_list = []
    for ele in new_list:
        file_VH = ele[:ele.index("|")]
        file_VH_list.append(file_VH)
    VV = open(os.path.join(Paths.main_path, "sentinel-filelistVV.txt"))
    new_list = VV.readlines()
    print(new_list)
    for ele in new_list:
        file_VV = ele[:ele.index("|")]
        file_VV_list.append(file_VV)

    rvi_list = []
    for i, rvi in enumerate(file_VH_list):
        mapcalc_rvi = Module("r.mapcalc")
        expression = f"= 4*(10^( {file_VH_list[i]} /10))/(10^( {file_VV_list[i]}/10)+10^( {file_VH_list[i]} /10))"
        mapcalc_rvi(overwrite=overwrite_bool,
                    expression=layername + str(i) + expression,
                    region="current")
        rvi_list.append(layername + str(i))

        print("---------------------------- RVI Info - Layer " + layername + str(i) + " ----------------------------")
        rvi_info = Module("r.info")
        rvi_info(map=layername + str(i))

    rvi_visualization = Module("g.gui.animation")
    rvi_visualization(raster=rvi_list)
