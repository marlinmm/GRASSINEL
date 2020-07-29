import os
from GEO450_GRASS_S1.user_data import *


def extract_files_to_list(path_to_folder, datatype):
    """
    function to extract files of given datatype from given directory and return as a list
    :param path_to_folder: string
        path to folder, where files are to be extracted from
    :param datatype: string
        datatype of files to return from given folder
    :return: new_list: list
        returns list of paths to files
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
    imports polygon from path given in user_data.py class Paths
    :return: shapelist
        returns polygons from given shapefile as a list
    """
    import fiona
    shape_list = []
    active_shapefile = fiona.open(Paths.boundary_path, "r")
    for i in range(0, len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
        shape_list.append(shapes)
    return shape_list


def subset_processed_data():
    """
    function to subset rasterdata using polygons from a shapefile and export the subset to a new folder
    all paths are given in user_data.py
    """
    import rasterio as rio
    import rasterio.mask
    import numpy as np
    ### install BanDiTS using: python3.6 -m pip install git+https://github.com/marlinmm/BanDiTS.git ###
    from BanDiTS.export_arr import functions_out_array
    import shutil

    subset_path = os.path.join(Paths.sen_processed_path, "subset/")
    if os.path.exists(subset_path):
        shutil.rmtree(subset_path)
    os.mkdir(subset_path)
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
        tmp1 = processed_file_list[k].index("_dir")
        tmp2 = len(processed_file_list[k])
        print(subset_path + processed_file_list[k][tmp1 + 5:tmp2 - 4])
        functions_out_array(outname=subset_path + processed_file_list[k][tmp1 + 5:tmp2 - 4] + "_subset.tif",
                            arr=out_image1,
                            input_file=processed_file_list[k], dtype=np.float32, ras_meta1=ras_meta1)
