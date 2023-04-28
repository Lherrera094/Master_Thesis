#!/usr/bin/env python
# coding: utf-8
# %%


# Developer: Luis Carlos Herrera Quesada
# Date: 28/04/2023
# Universidad Carlos III de Madrid


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#read the file profiles.dat
def read_data_iota(file):
    data = pd.read_csv(f"{file}/profiles.dat",sep="\t")
 
    return data

#Obtain all coupling in the iota boundaries
def resonance_coupling(dataframe):
    #iota_min = min(abs(dataframe["       iota"]))
    iota_max = max(abs(dataframe["       iota"]))
    iota_min = 1.2
    
    n_families = np.linspace(1,17,17)
    
    #iota_min < iota_max ------> 1/iota_min > 1/iota_max
    max_m = n_families/iota_min
    min_m = n_families/iota_max
    
    #To mark the those n/m values that are out of the iota boundaries for the device
    marker = abs(np.ceil(max_m) - np.ceil(min_m))
    m_min = np.ceil(min_m)
    m_max = np.floor(max_m)
    
    #dats = np.transpose([max_m,min_m,np.ceil(max_m),np.ceil(min_m),marker])
    #print(dats)
    
    m = m_min #minumuum value of m that satisfy to be in the iota boundaries
    i = n_families/m
    
    #creates a first array with the single minumum m values that fits in the iota boundaries
    new_array = np.transpose([n_families,min_m,max_m,m,marker,i,i])
    new_array_1 = pd.DataFrame(new_array,columns = ["n","min_m","max_m","m","marker","n/m", "n/m marked"])
    
    #This next line takes into account if more values of m makes n/m be inside iota profile
    for i in range(len(new_array)):
        
        if new_array_1["marker"][i] > 1:
            
            #print(new_array_1["marker"][i]-1,new_array_1["n"][i])
            
            for l in range(int(new_array_1["marker"][i])-1):
                
                row_to_copy = new_array_1.loc[i]
                new_row = row_to_copy.copy()
                new_row["m"],new_row["n/m"] = new_row["m"] + (l+1),new_row["n"]/(new_row["m"] + (l+1))
                
                new_array_1 = new_array_1.append(new_row, ignore_index=True)
    
    clean_indx = new_array_1[new_array_1.marker.isin([0.0])].index
    new_array_1.loc[clean_indx, "m"] = 0.0
    new_array_1.loc[clean_indx, "n/m marked"] = np.nan
    
    new_array_1 = new_array_1.sort_values('n',ascending=True)
    
    return iota_max, iota_min, new_array_1


#General Plot of the iota
def plot_iota(dataframe,iota_value):
    plt.plot(dataframe["        r"],dataframe["       iota"],
             "darkcyan",label = r"$\iota$ profile",linewidth = 1.5)
    
    plt.title(f"$\iota$= ${iota_value}$ Profile",size=22)
    plt.ylabel(r"$\iota$",fontsize=20)
    plt.xlabel("r/a",fontsize=20)
    plt.grid(True)
    plt.show()
    plt.savefig(f"{iota_value}/TJII_iota.jpg",dpi=600)


#Obtain the coupled toroidal families
def get_families(coupl,period):
    n_fam = {}
    for n in coupl["n"]:
        key = n%period
        if key not in n_fam:
            n_fam[key] = []
        n_fam[key].append(n)
        
    return n_fam


#Plot of the posible resonant modes
def plot_resonant_modes(coupl,period,folder,pos,dataframe,s):
    iota_min = min(abs(dataframe["       iota"]))
    iota_max = max(abs(dataframe["       iota"]))
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(10,5))
    
    n_fam = get_families(coupl,period)
    x = np.linspace(1,18,18)
    y = np.linspace(1,15,15)
    new_res_df = coupl.dropna()
    
    ax1.axhline(y=iota_min,color='darkcyan')
    ax1.axhline(y=iota_max,color='darkcyan')
    
    for i in n_fam:
        res_modes = new_res_df[new_res_df["n"].isin(n_fam[i])]
        lab = res_modes["n"].values
        lab = np.unique(lab)
        ax1.plot(res_modes["n"],res_modes["n/m"],"o",label=f"n={lab}" if len(res_modes["n"]) != 0 else None)
        ax2.plot(res_modes["n"],res_modes["m"],"o",label=f"n={lab}" if len(res_modes["n"]) != 0 else None)
    
    #Axis 1:Figure i vs n
    ax1.set_title(f"Toroidal Families ($\iota$={round(iota_max,2)})",size=19)
    ax1.set_xlabel("Toroidal $n$",fontsize=20)
    ax1.set_ylabel(r"$\iota$ Boundaries",fontsize=20)
    ax1.set_xticks(x)
    ax1.tick_params(axis='both',labelsize=14)
    ax1.set_xlim([min(new_res_df["n"])-1,max(new_res_df["n"])+1])
    ax1.legend(loc=pos,prop={'size':s}) 
    ax1.grid(True)
    
    
    #Axis 2: Figure m vs n
    ax2.set_title(f"Toroidal/Poloidal Couplings",size=19)
    ax2.set_ylabel(f"Poloidal $m$",fontsize=20)
    ax2.set_xlabel(f"Toroidal $n$",fontsize=20)
    ax2.set_xticks(x)
    ax2.set_yticks(y)
    ax2.tick_params(axis='both',labelsize=14)
    ax2.set_xlim([min(new_res_df["n"])-1,max(new_res_df["n"])+1])
    ax2.set_ylim([min(new_res_df["m"])-1,max(new_res_df["m"])+1])
    ax2.legend(loc='upper left',prop={'size':10})
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(f"{folder}/{round(iota_max,2)}_iota_Couplings.png",dpi=600)


#Plot of all iota profiles to study
def plot_all_iota(set_df):
    #read all dataframes from diferent profiles
    y = [1.1,1.25,1.5,1.75,2.0,2.25]
    df_exp = read_data_iota(set_df[0])
    df_1 = read_data_iota(set_df[1])
    df_2 = read_data_iota(set_df[2])
    df_3 = read_data_iota(set_df[3])
    df_4 = read_data_iota(set_df[4])
    
    lab = set_df[0].split("/")
    max_i_1 = round(max(df_1["       iota"]),2)
    max_i_2 = round(max(df_2["       iota"]),2)
    max_i_3 = round(max(df_3["       iota"]),2)
    max_i_4 = round(max(df_4["       iota"]),2)
    
    #Plot all profiles
    plt.plot(abs(df_exp["        r"]),abs(df_exp["       iota"]), "black",label = f"{lab[0]} profile",
             linewidth = 1.5)
    plt.plot(df_1["        r"],df_1["       iota"],"blue",label = f"$\iota$ {max_i_1} profile",
             linewidth = 1.5)
    plt.plot(df_2["        r"],df_2["       iota"],"red",label = f"$\iota$ {max_i_2} profile",
             linewidth = 1.5)
    plt.plot(df_3["        r"],df_3["       iota"],"violet",label = f"$\iota$ {max_i_3} profile",
             linewidth = 1.5)
    plt.plot(df_4["        r"],df_4["       iota"],"orange",label = f"$\iota$ {max_i_4} profile",
             linewidth = 1.5)
    
    plt.title(f"$\iota$ Profiles",size=22)
    plt.ylabel(r"$\iota$",fontsize=20)
    plt.xlabel("r/a",fontsize=20)
    plt.yticks(y)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1, 1.22), loc='upper right',prop={'size':9})
    plt.show()
    plt.savefig(f"TJII_iota_full.jpg",dpi=600)
