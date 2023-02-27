# Author: Austin Shih
# Date: 20 Feb 2022

""" Downloads csv file from the web and saves contents to a local directory.
Usage: download.py --out_file=<out_file>
Options:
--out_file=<out_file>     Path to write the contents to 
"""

# python src/download.py --out_file=data/raw/nbi_raw.csv

import requests
from docopt import docopt
import os
import pandas as pd

opt = docopt(__doc__)

def main(out_file):
    
    # file updated January 13, 2023
    url = 'https://opendata.arcgis.com/api/v3/datasets/2467101f84e447aebf164a6680d2f59d_0/downloads/data?format=csv&spatialRefId=3857&where=1%3D1'
    #check if URL is valid
    try:
        print('checking URL...') 
        request = requests.get(url, stream=True)
        request.status_code == 200
        print("URL valid")
    except Exception as ex: 
        print("the URL provided is invalid")
        print(ex)
    
    print('downloading csv file...')
    data = pd.read_csv(url, header=0)
    try:
      data.to_csv(out_file, index = False)
    except:
      os.makedirs(os.path.dirname(out_file))
      data.to_csv(out_file, index = False)

if __name__ == "__main__":
    main(opt['--out_file'])