import os
import glob
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def combineall(name):
    dir = "R:/CPI_SD/Online Pricing/Regular Price Collection/Watsons/Data/"
    os.chdir(dir+name)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    # export to csv
    os.chdir(dir)
    combined_csv.to_csv(name+"-combined.csv", index=False, encoding='utf-8-sig')

combineall("watsons-mask")
