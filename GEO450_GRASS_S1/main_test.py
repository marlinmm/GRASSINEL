import os
from GEO450_GRASS_S1.new_setup import *
from GEO450_GRASS_S1.python_setup import *
######## add user directory ########

main_dir = os.path.abspath("/home/user/Desktop/GEO450_main_dir")


######## create needed directories ########

grass_dir = os.path.join(main_dir, 'grass_dir')
sen_down_dir = os.path.join(main_dir, 'sen_down_dir')
sen_processed_dir = os.path.join(main_dir, 'sen_processed_dir')

if not os.path.exists(grass_dir):
    os.makedirs(grass_dir)
if not os.path.exists(sen_down_dir):
    os.makedirs(sen_down_dir)
if not os.path.exists(sen_processed_dir):
    os.makedirs(sen_processed_dir)

class Paths(object):
    grass_path = grass_dir
    send_down_path = sen_down_dir
    sen_processed_path = sen_processed_dir

GRASSBIN_import()
grass_setup(location_name="GEO450_test1", crs=32632, grass_version="grass79")