from GEO450_GRASS_S1.grass_functionality import *
from GEO450_GRASS_S1.grass_setup import *
from GEO450_GRASS_S1.S1_preprocessing import *
from datetime import datetime


def main():
    ########## GRASS SETUP FUNCTION(S) #############
    grass_setup()
    # import_shapefile(path_to_shape=Paths.boundary_path, overwrite_bool=True)

    ######### SENTINEL DOWNLOAD FUNCTION(S) #############
    # sen_download(start_time="2020-05-01", end_time="2020-05-04", sort_by="ingestiondate")
    # sen_download_new(start_time="2020-05-01", end_time="2020-05-30", sort_by="ingestiondate", relative_orbit_number=168)

    # ########## SENTINEL PREPROCESSING FUNCTION(S) #############
    # pyroSAR_processing(start_time=start_time, target_resolution=50, target_CRS=32632, terrain_flat_bool=False, remove_therm_noise_bool=False)
    # subset_import(overwrite_bool=True, output="raster", polarization_type=["VH", "VV"])

    # ########## GRASS SPACE TIME CUBE FUNCTION(S) #############
    # create_stc(overwrite_bool=True, output="stc", polarization_type=["VH", "VV"], stc_info_bool=False, stc_statistics_bool=False)
    # visualize_stc(output="stc", polarization_type=["VV", "VH"], stc_animation_bool=False, stc_timeline_bool=False)

    # ########## GRASS ANALYSIS FUNCTION(S) #############
    raster_algebra(basename="product", layername="result", expression=" = stcVH*stcVV", overwrite_bool=True)
    rvi_mapcalc(layername="rvi", overwrite_bool=True)


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("processing-time = ", end_time - start_time, "Hr:min:sec")