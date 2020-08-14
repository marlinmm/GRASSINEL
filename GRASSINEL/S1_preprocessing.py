from GRASSINEL.support_functions import *


def pyroSAR_processing(down_path, processed_path, target_resolution, target_CRS, terrain_flat_bool, remove_therm_noise_bool):
    """
    aims at providing a complete solution for the scalable organization and processing of SAR satellite data
    Copyright by John Truckenbrodt
    :param down_path: string
        set path to download directory of Sen-1 data
    :param processed_path: string
        set path to directory of processed Sen-1 data
    :param target_resolution: int
        target output resolution of processed Sentinel-1 image
    :param target_CRS: int
        target output coordinate reference system
    :param terrain_flat_bool: boolean
        boolean to activate or deactivate terrain flattening
    :param remove_therm_noise_bool: boolean
        boolean to activate or deactivate thermal noise removal
    """
    from datetime import datetime
    from pyroSAR.snap.util import geocode
    print(down_path)
    start_time = datetime.now()
    sentinel_file_list = extract_files_to_list(down_path, datatype=".zip")
    for i, file in enumerate(sentinel_file_list):
        geocode(infile=file, outdir=processed_path, tr=int(target_resolution), t_srs=int(target_CRS),
                terrainFlattening=terrain_flat_bool, removeS1ThermalNoise=remove_therm_noise_bool)

        interval_time = datetime.now()
        print("file " + str(i + 1) + " of " + str(len(sentinel_file_list)) + " processed in " +
              str(interval_time - start_time) + " Hr:min:sec")
    subset_processed_data()
