from GEO450_GRASS_S1.support_functions import *

def pyroSAR_processing(start_time, target_resolution, target_CRS, terrain_flat_bool, remove_therm_noise_bool):
    """
    aims at providing a complete solution for the scalable organization and processing of SAR satellite data
    Copyright by John Truckenbrodt
    TODO: ADD DOCSTRINGS!!!
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

