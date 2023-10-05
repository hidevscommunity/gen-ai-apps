# util function to extract coordinates from Mirxes list of supplier data to be used in streamlit folium map
import os 
import pandas as pd
import numpy as np
import json

PATH_TO_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
FILE_NAME = 'supplier_coordinates.json'
PATH_TO_COORDINATES_JSON  = os.path.join(PATH_TO_SRC, FILE_NAME)

# extract coords
class Importer:
    @classmethod
    def import_coordinates(cls) -> list[dict]:
        """
        Returns List of Json 

        Example output:
        [
            {"BP Code":"V000378","BP Name":"9 Koi Marketing Pte Ltd","lat":1.3871789,"lng":103.8272431},
            {"BP Code":"V000276","BP Name":"A*Star Research Entities","lat":1.2996123,"lng":103.7875984},
            {"BP Code":"V000155","BP Name":"Accelerate Technologies Pte Ltd","lat":1.2996123,"lng":103.7875984},
            {"BP Code":"V000712","BP Name":"Accucap MSC Sdn Bhd","lat":3.1075064,"lng":101.6467674},
        ]
        
        """
        with open(PATH_TO_COORDINATES_JSON, 'r') as f:
            coordinates = json.load(f)
        print(type(coordinates))
        return coordinates

# Test
if __name__ == '__main__':
    Importer.import_coordinates()