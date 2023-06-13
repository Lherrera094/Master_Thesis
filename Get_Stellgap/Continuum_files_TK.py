#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# %%

def extract_continuum(save_file):
    
    files = os.listdir(f"{save_file}")
    
    #Creates Continuum folder to save 
    if not os.path.exists(f"{save_file}/Continuo/"):
        os.mkdir(f"{save_file}/Continuo/")
    
    #search for alfven_post file
    for f in files:
        if f == "alfven_post.xlsx":
            alfven_file = pd.read_excel(f"{save_file}/{f}")
    
    #Split the alfven_post by n_mode number and save the file as txt
    for i in range(1,18):
        new_df = alfven_file[alfven_file["n_mode"] == -i]
        new_df.to_csv(f"{save_file}/Continuo/n = {abs(i)}.txt",sep="\t",index=False)
    
    return alfven_file

