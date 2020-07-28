from GEO450_GRASS_S1.grass_functionality import *
from datetime import datetime

# TODO: DEFINE USER DEPENDENT INPUT PATHS AND FILES -> HERE or in USER_DATA.py !?!?!?

def main():
    grass_setup()
    # import_shapefile(path_to_shape=Paths.boundary_path, overwrite_bool=True)
    # sen_download(start_time="2020-05-01", end_time="2020-05-04", sort_by="ingestiondate")
    # sen_download_new(start_time="2020-05-01", end_time="2020-05-30", sort_by="ingestiondate", relative_orbit_number=168)
    # pyroSAR_processing(start_time=start_time, target_resolution=50, target_CRS=32632, terrain_flat_bool=False, remove_therm_noise_bool=False)
    #subset_import(subset_path="/media/user/2nd_disk/sen_processed_dir/subset",
    #              filelist_path="/home/user/Desktop/GRASS Jena Workshop/sentinel-filelistVV.txt", overwrite_bool=True, output="rasterVV", polarization_type="VV")
    create_stc(overwrite_bool=True, filelist_path="/home/user/Desktop/GRASS Jena Workshop/sentinel-filelistVH.txt", output="stcVH")
    #t_rast_algebra(basename="product1", expression="result1 =(stcVH*stcVV)/stcVH")


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("processing-time = ", end_time - start_time, "Hr:min:sec")