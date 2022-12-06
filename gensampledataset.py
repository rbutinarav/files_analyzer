#this code generates a sample dataset for the purpose of testing the code
#it checke if a dataset folder exists, if not it creates it
#then creates a sample dataset with 10 files, 5 columns and 2000 rows each
#the files are named file1.csv, file2.csv, etc.

import os
import pandas as pd
import numpy as np

#check if dataset folder exists, if not create it
if not os.path.exists('dataset'):
    os.makedirs('dataset')
    
#generate 10 files with 5 columns and 2000 rows each
for i in range(1,11):
    df = pd.DataFrame(np.random.randint(0,100,size=(2000, 5)), columns=list('ABCDE'))
    df.to_csv('dataset/file'+str(i)+'.csv', index=False)
