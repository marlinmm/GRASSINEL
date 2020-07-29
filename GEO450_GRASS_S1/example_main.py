from GEO450_GRASS_S1.grass_functionality import *
from datetime import datetime

# TODO: DEFINE USER DEPENDENT INPUT PATHS AND FILES -> HERE or in USER_DATA.py !?!?!?

def main():
    grass_setup()
    # import_shapefile(path_to_shape=Paths.boundary_path, overwrite_bool=True)
    # sen_download(start_time="2020-05-01", end_time="2020-05-04", sort_by="ingestiondate")
    # sen_download_new(start_time="2020-05-01", end_time="2020-05-30", sort_by="ingestiondate", relative_orbit_number=168)
    # pyroSAR_processing(start_time=start_time, target_resolution=50, target_CRS=32632, terrain_flat_bool=False, remove_therm_noise_bool=False)
    #subset_import(overwrite_bool=True, output="raster", polarization_type=["VH", "VV"])
    #create_stc(overwrite_bool=True, output="stc", polarization_type=["VV", "VH"], stc_info=True, stc_statistics=True)
    visualize_stc(output="stc", polarization_type=["VV", "VH"], stc_animation=True, stc_timeline=False)
    # t_rast_algebra(basename="product2", expression="result2 =(stcVH*stcVV)/stcVH")


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("processing-time = ", end_time - start_time, "Hr:min:sec")