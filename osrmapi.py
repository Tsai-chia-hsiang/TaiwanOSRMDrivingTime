from dicttool import *
import os
from routingpy import OSRM
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

    def _single_source(self, srcinfo:list, idslices:list, cooslices:list)->dict:
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
        
            r = self._single_source([srcid, nodedict[srcid]],idslices, cooslices)
            writejson(r,resultsave)
        
