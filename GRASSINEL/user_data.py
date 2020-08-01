import os


def user_data():
    """
    return: location_name, crs, grass_version, main_dir, grass_dir, sen_down_dir, sen_processed_dir, subset_dir,
            boundary_shape
            self-explanatory returns, for acces through the Path classes "GrassData" and "Paths"
    """
    ######## add user data for grass setup ########
    location_name = "GRASSINEL_test"
    crs = "32632"
    grass_version = "grass79"

    ######## add user directory ########
    boundary_shape = "/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_boundary.gpkg"
    main_dir = os.path.abspath("/home/user/Desktop/GRASSINEL_dir")
    data_dir = os.path.abspath("/media/user/2nd_disk")

    ######## create needed directories ########
    grass_dir = os.path.join(main_dir, 'grass_dir')
    sen_down_dir = os.path.join(data_dir, 'sen_down_dir')
    sen_processed_dir = os.path.join(data_dir, 'sen_processed_dir')
    subset_dir = os.path.join(sen_processed_dir, "subset")

    if not os.path.exists(grass_dir):
        os.makedirs(grass_dir)
    if not os.path.exists(sen_down_dir):
        os.makedirs(sen_down_dir)
    if not os.path.exists(sen_processed_dir):
        os.makedirs(sen_processed_dir)

    return location_name, crs, grass_version, main_dir, grass_dir, sen_down_dir, sen_processed_dir, subset_dir,\
           boundary_shape


class GrassData(object):
    location_name, crs, grass_version = user_data()[0:3]

class Paths(object):
    main_path, grass_path, sen_down_path, sen_processed_path, subset_path, boundary_path = user_data()[3:10]
