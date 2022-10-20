import os
from dicttool import *
from AttractionData import AttractionDataset as attrd
from osrmapi import Router

def each_region():

    attractions = attrd(
        csvfilepath=os.path.join(".", "cluster_with_coo.csv"),
        region=loadjson(jsonfilepath=os.path.join(".","tw_region.json"))
    )

    resultroot=os.path.join(".","osmdist")
    if os.path.exists(resultroot):
        os.mkdir(resultroot)
    
    router = Router()
    for k in attractions.twregion.keys():
        print(k)
        savedir = os.path.join(resultroot, f"{k}")
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        
        print(savedir)
        pid_coo = attractions.extract_places_coordinate(target_region=k)
        router.routing(pid_coo, savedir, batchsize=250)

def taiwan_main_island():
    attractions = attrd(
        csvfilepath=os.path.join(".", "cluster_with_coo.csv"),
        region=loadjson(jsonfilepath=os.path.join(".","tw_region.json"))
    )
    outlying = ["Penghu", "Kinmen","Lienchiang","Greenisland", "Lanyu"]
    main_island = list(t for t in attractions.twregion.keys() if t not in outlying )
    pid_coo = attractions.extract_places_coordinate(target_region=main_island)
    savedir = os.path.join("osmdist", "Allpair")
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    
    router= Router()
    router.routing(pid_coo, saveingdir=savedir,batchsize=250)

if __name__ == "__main__":
    taiwan_main_island()