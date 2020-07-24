from GEO450_GRASS_S1.grass_functionality import *
from datetime import datetime


def main():
    grass_setup()
    #import_shapefile(overwrite=True)
    #sen_download(start_time="2020-06-01", end_time="2020-06-02", sort_by="ingestiondate")
    #test()
    pyroSAR_processing()


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("extract_files-time = ", end_time - start_time, "Hr:min:sec")