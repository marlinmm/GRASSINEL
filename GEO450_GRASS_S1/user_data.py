import os

######## add user data for grass setup ########
location_name = "GEO450_test1"
crs = "32632"
grass_version = "grass79"

######## add user directory ########
boundary_shape = "/home/user/Desktop/GRASS Jena Workshop/geodata/osm/jena_boundary.gpkg"
main_dir = os.path.abspath("/home/user/Desktop/GEO450_main_dir")
data_dir = os.path.abspath("/media/user/2nd_disk")
######## create needed directories ########

grass_dir = os.path.join(main_dir, 'grass_dir')
sen_down_dir = os.path.join(data_dir, 'sen_down_dir')
sen_processed_dir = os.path.join(data_dir, 'sen_processed_dir')

if not os.path.exists(grass_dir):
    os.makedirs(grass_dir)
if not os.path.exists(sen_down_dir):
    os.makedirs(sen_down_dir)
if not os.path.exists(sen_processed_dir):
    os.makedirs(sen_processed_dir)


class GRASS_data(object):
    location_name = location_name
    crs = crs
    grass_version = grass_version


class Paths(object):
    grass_path = grass_dir
    send_down_path = sen_down_dir
    sen_processed_path = sen_processed_dir
    boundary_path = boundary_shape