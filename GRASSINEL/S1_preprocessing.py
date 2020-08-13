from GRASSINEL.support_functions import *


def pyroSAR_processing(start_time, target_resolution, target_CRS, terrain_flat_bool, remove_therm_noise_bool):
    """
    aims at providing a complete solution for the scalable organization and processing of SAR satellite data
    Copyright by John Truckenbrodt
    :param start_time: datetime.datetime
        timing parameter for run duration
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

    sentinel_file_list = extract_files_to_list(Paths.sen_down_path, datatype=".zip")
    for l, file in enumerate(sentinel_file_list):
        geocode(infile=file, outdir=Paths.sen_processed_path, tr=target_resolution, t_srs=target_CRS,
                terrainFlattening=terrain_flat_bool, removeS1ThermalNoise=remove_therm_noise_bool)

        interval_time = datetime.now()
        print("file " + str(l + 1) + " of " + str(len(sentinel_file_list)) + " processed in " + str(
            interval_time - start_time) + " Hr:min:sec")
    subset_processed_data()
