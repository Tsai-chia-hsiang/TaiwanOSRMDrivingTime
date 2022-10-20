import os
import pandas as pd

class AttractionDataset():

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

    def extract_places_coordinate(self, target_region:str|list="all")->dict:
        
        def extraction_places_coo(df:pd.DataFrame)->dict:
            placeidlist = df['placeid'].tolist()
            lnglist = df['lng'].tolist()
            latlist = df['lat'].tolist()
            lng_lat =[[lnglist[i], latlist[i]] for i in range(len(lnglist))]
            return dict(zip(placeidlist,lng_lat))

        if target_region == "all":
            return extraction_places_coo(self.df)
        if isinstance(target_region, list):
            print(target_region)
            targetdf = pd.concat( list((self.regiondf[t] for t in target_region)))
            return extraction_places_coo(targetdf)
        
        return extraction_places_coo(self.regiondf[target_region])
    
