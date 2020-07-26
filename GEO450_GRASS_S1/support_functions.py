import os
from GEO450_GRASS_S1.user_data import *

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


def subset_processed_data():
    """

    TODO: do all this internall in GRASS

    """
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
