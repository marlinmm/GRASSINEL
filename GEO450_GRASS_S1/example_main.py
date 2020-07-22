from GEO450_GRASS_S1.grass_functionality import *

def main():
    grass_setup()
    #sen_download(start_time="2020-06-01", end_time="2020-06-02", sort_by="ingestiondate")
    #import_shapefile()
    #test()
    pyroSAR_processing()


if __name__ == "__main__":
    main()