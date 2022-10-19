from dicttool import *
import os
from routingpy import OSRM
import pandas as pd
from tqdm import tqdm

class Router():
    def __init__(self):
        self.client = OSRM(
            base_url="https://routing.openstreetmap.de/routed-car"
        )
        self.__pbar = None

    def _gen_batch(self, nodedict:dict, batchsize)->tuple:
        coolist = list(nodedict.values())
        idlist = list(nodedict.keys())
        idslices = []
        cooslices = []
        for i in range(0, len(coolist), batchsize):
            idslices.append(idlist[i:i+batchsize])
            cooslices.append(coolist[i:i+batchsize])
        return idslices, cooslices

    def single_source(self, srcinfo:list, idslices:list, cooslices:list)->dict:
        nodelinks = {}
        batch_count =0
        for Dstidbatch, Coobatch in zip(idslices,cooslices):
            
            dstidbatch = [srcinfo[0]]+Dstidbatch
            coobatch = [srcinfo[1]]+Coobatch
            
            batch_count += 1
            try:
                r = self.client.matrix(locations=coobatch,sources=[0])
                self.__pbar.set_postfix_str(f"{srcinfo[0]}_{batch_count} ok")
            except:
                self.__pbar.set_postfix_str(f"{srcinfo[0]}_{batch_count} err")
                r = self.client.matrix(locations=coobatch,sources=[0])
        
            d = r.distances
            t = r.durations
            for j , dstid in enumerate(dstidbatch):
                nodelinks[dstid] = {
                    'time':t[0][j],
                    'dist':d[0][j]
                }
        return nodelinks


    def routing(self, nodedict:dict, saveingdir:os.PathLike,batchsize = 250)->None:
        
        idslices , cooslices= self._gen_batch(nodedict, batchsize)
        self.__pbar = tqdm(list(nodedict.keys()))
        for i, srcid in enumerate(self.__pbar):
            resultsave = os.path.join(saveingdir, f"{srcid}.json")
            if os.path.exists(resultsave):
                self.__pbar.set_postfix_str(f"gotten {srcid}")
                continue
        
            r = self.single_source([srcid, nodedict[srcid]],idslices, cooslices)
            writejson(r,resultsave)
        

class attractiondataset():

    def __init__(self, csvfilepath:os.PathLike, region:dict) -> None:
        self.df = pd.read_csv(csvfilepath)
        self.twregion = region
        self.regiondf = self.__divide_according_regions()        
    
    @staticmethod
    def write_data(df, writingpath)->None:
        df.to_csv(writingpath, encoding='utf-8', index=False)

    def __divide_according_regions(self)->dict:
        diff_region = {}
        for region, name in self.twregion.items():
            diff_region[region] = self.df[self.df['region2'].isin(name['chi2'])]
        return diff_region

    def extract_places_coordinate(self, target_region:str="all")->dict:
        
        def extraction_places_coo(df:pd.DataFrame)->dict:
            placeidlist = df['placeid'].tolist()
            lnglist = df['lng'].tolist()
            latlist = df['lat'].tolist()
            lng_lat =[[lnglist[i], latlist[i]] for i in range(len(lnglist))]
            return dict(zip(placeidlist,lng_lat))

        if target_region == "all":
            return extraction_places_coo(self.df)
        return extraction_places_coo(self.regiondf[target_region])
    

def main():

    attractions = attractiondataset(
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


def testing():
    client = OSRM(base_url="https://routing.openstreetmap.de/routed-car")
    r = client.matrix(
        locations=[[121.50617, 25.24749], [121.51787, 25.28422]],
        sources=[0]
    )
    print(r.distances)
    print(r.durations)

if __name__ == "__main__":
    main()
    #testing()
