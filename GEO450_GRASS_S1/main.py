from GEO450_GRASS_S1.example import *
from GEO450_GRASS_S1.python_setup import *
from GEO450_GRASS_S1.test import *

def main():
    ############## LINUX IMPORT PATHS ###############
    ### Linux path <- add path here for each Linux user and do not overwrite!
    gisdb = '/home/user/grassdata'

    ### Windows path <- add path here for each Windows user and do not overwrite!
    # gisdb = 'F:/GEO450_GRASS/test_python'

    ######### SET GRASS LOCATION AND MAPSET #########
    location = "test3"
    mapset = "PERMANENT"

    GRASSBIN_import()
    create_GRASS_GIS_location(gisdb, location, mapset)


    ############# FUNCTIONS TO BE EXECUTED ##############
    ogrimport()
    sentineldownload()





if __name__== "__main__" :
    main()