#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid
# %%


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#Read Alfven data
def read_dataframe(x):
    exp_df = pd.read_excel(f"{x}/results_exp_{x}.xlsx")    #Experimental Profile
    
    OnA_df = pd.read_excel(f"{x}/results_OnA_{x}.xlsx")    #On Axis Profile
    
    OfA_df = pd.read_excel(f"{x}/results_OfA_{x}.xlsx")    #Off Axis Profile
    
    hg_df = pd.read_excel(f"{x}/results_HG_{x}.xlsx")      #High Gradient Profile 
    
    lg_df = pd.read_excel(f"{x}/results_LG_{x}.xlsx")      #Low Gradient Profile
    
    return exp_df,OnA_df,OfA_df,hg_df,lg_df


#Read Continuum
def read_continuum(x):
    df = pd.read_csv(f"Continuum/output_column_n={x}.txt", sep="\t")
    df.columns = ["r","freq"]
    df["r"] = np.sqrt(df["r"]) 
    df = df.drop(df[df["freq"] <= 10].index)
    return df


def data_analysis(fam):
    exp_df,OnA_df,OfA_df,hg_df,lg_df = read_dataframe(fam)
    
    markers = {'HAE':"o","TAE/EAE":"^",'GAE':"s"}
    
    dictionary = {
        "n3": {
            "title": "n=3,7,11,15",
            "continuum": [3,7,11,15],
            "colors": ["k","green","indigo","orange"],
            "ylim_f":[0,300],
            "ylim_gr":[0,1],
            "position":"upper left"
        },
        "n5": {
            "title": "n=5,9,13,17",
            "continuum": [1,5,9,13],
            "colors": ["blue","green","mediumpurple","goldenrod"],
            "ylim_f":[0,300],
            "ylim_gr":[0,1],
            "position":"upper left"
        },
        "n6": {
            "title": "n=6,10,14",
            "continuum": [6,10,14],
            "colors": ["darkcyan","red","dimgrey"],
            "ylim_f":[0,370],
            "ylim_gr":[0,1],
            "position":"lower left"
        },
        "n8": {
            "title": "n=8,12,16",
            "continuum": [4,8,12],
            "colors": ["firebrick","green","mediumpurple"],
            "ylim_f":[0,370],
            "ylim_gr":[0,1.2],
            "position":"lower left"
        }
    }
    
    return exp_df, OnA_df, OfA_df, hg_df, lg_df, markers, dictionary[fam],fam


def plot_Freq_fam(df_exp,df_OnA,df_OfA,df_hg,df_lg,mark,dictionary,x):
    
    df_exp_g = df_exp.groupby(["Alfvén_mode"])
    for af,df in df_exp_g:
        ex = df_exp[df_exp["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="black",marker=mark[af],facecolors='none',alpha=2,
                    s = 60,label="Experimental" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
        
    df_OnA_g = df_OnA.groupby(["Alfvén_mode"])
    for af,df in df_OnA_g:
        ex = df_OnA[df_OnA["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="blue",marker=mark[af], facecolors='none',alpha=2,
                   s = 60, label="On Axis" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
    
    
    df_OfA_g = df_OfA.groupby(["Alfvén_mode"])
    for af,df in df_OfA_g:
        ex = df_OfA[df_OfA["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="darkgreen",marker=mark[af], facecolors='none',alpha=2,
                   s = 60, label="OFF Axis" if af == "HAE" else None) 
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
        

    df_lg_g = df_lg.groupby(["Alfvén_mode"])
    for af,df in df_lg_g:
        ex = df_lg[df_lg["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="darkorange",marker=mark[af], facecolors='none', alpha=2,
                   s = 60, label="Low Gradient" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af],s = 25)
        plt.clim(0,1)
    
    df_hg_g = df_hg.groupby(["Alfvén_mode"])
    for af,df in df_hg_g:
        ex = df_hg[df_hg["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="red",marker=mark[af], facecolors='none',alpha=2,
                   s = 60, label="High Gradient" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
        
    plt.colorbar()
    for i in range(len(dictionary['continuum'])):
        data = read_continuum(dictionary['continuum'][i])
        plt.plot(data["r"],data["freq"],"o",color=dictionary['colors'][i],markersize=1)
        
    plt.title(f"AE Frequency {dictionary['title']}")
    plt.ylabel("$f$(kHz)")
    plt.xlabel("r/a")
    plt.xlim([0.1,1])
    plt.ylim(dictionary['ylim_f'])
    plt.legend(loc=dictionary['position'],prop={'size':7})
    plt.show()
    plt.savefig(f"{x}/Frequency_{dictionary['title']}_Analysis.jpg",dpi=400)


def plot_Freq_motion(df_exp,df_OnA,df_OfA,df_hg,df_lg,mark,dictionary,x):
    
    df_exp_g = df_exp.groupby(["Alfvén_mode"])
    for af,df in df_exp_g:
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="black",marker=mark[af],
                    s = 60,label="Experimental" if af == "HAE" else None)
        
    df_OnA_g = df_OnA.groupby(["Alfvén_mode"])
    for af,df in df_OnA_g:
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="blue",marker=mark[af], 
                   s = 60, label="On Axis" if af == "HAE" else None)
    
    
    df_OfA_g = df_OfA.groupby(["Alfvén_mode"])
    for af,df in df_OfA_g:
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="darkgreen",marker=mark[af], 
                   s = 60, label="OFF Axis" if af == "HAE" else None) 
        

    df_lg_g = df_lg.groupby(["Alfvén_mode"])
    for af,df in df_lg_g:
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="darkorange",marker=mark[af], 
                   s = 60, label="Low Gradient" if af == "HAE" else None)
    
    df_hg_g = df_hg.groupby(["Alfvén_mode"])
    for af,df in df_hg_g:
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="red",marker=mark[af],
                   s = 60, label="High Gradient" if af == "HAE" else None)
        
    for i in range(len(dictionary['continuum'])):
        data = read_continuum(dictionary['continuum'][i])
        plt.plot(data["r"],data["freq"],"o",color=dictionary['colors'][i],markersize=1)
        
    plt.title(f"AE Frequency {dictionary['title']}")
    plt.ylabel("$f$(kHz)")
    plt.xlabel("r/a")
    plt.xlim([0.1,1])
    plt.ylim(dictionary['ylim_f'])
    plt.legend(loc=dictionary['position'],prop={'size':7})
    plt.show()
    plt.savefig(f"{x}/Frequency_{dictionary['title']}_move_Analysis.jpg",dpi=400)


# ## Analysis by Profile
def plot_profile_F_analysis(df_prof_3,df_prof_5,df_prof_6,df_prof_8,mark,new_title,dictionary,pos):
    if not os.path.exists("All_families_plot"):
        os.makedirs("All_families_plot")
    
    #Max Values from all profiles
    df3 = get_max_values(df_prof_3,"n3")
    df5 = get_max_values(df_prof_5,"n5")
    df6 = get_max_values(df_prof_6,"n6")
    df8 = get_max_values(df_prof_8,"n8")
    full_df = pd.concat([df3,df5,df6,df8],axis = 1)
    full_df.to_excel(f"All_families_plot/{new_title} Maximum Values.xlsx")
    
    #Plot for all profiles
    df_prof_3_g = df_prof_3.groupby(["Alfvén_mode"])
    for af,df in df_prof_3_g:
        ex = df_prof_3[df_prof_3["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="black",marker=mark[af], s = 60,
                    label="n=3,7,11,15" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
    
    df_prof_5_g = df_prof_5.groupby(["Alfvén_mode"])
    for af,df in df_prof_5_g:
        ex = df_prof_5[df_prof_5["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="blue",marker=mark[af], s = 60,
                   label="n=5,9,13,17" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
    
    df_prof_6_g = df_prof_6.groupby(["Alfvén_mode"])
    for af,df in df_prof_6_g:
        ex = df_prof_6[df_prof_6["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="green",marker=mark[af], s = 60,
                   label="n=6,10,14" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
    
    df_prof_8_g = df_prof_8.groupby(["Alfvén_mode"])
    for af,df in df_prof_8_g:
        ex = df_prof_8[df_prof_8["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="orange",marker=mark[af], s = 60,
                   label="n=8,12,16" if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 25)
        plt.clim(0,1)
    
    for i in range(len(dictionary['continuum'])):
        data = read_continuum(dictionary['continuum'][i])
        plt.plot(data["r"],data["freq"],"o",color=dictionary['colors'][i],markersize=1)
    
    plt.colorbar()
    plt.title(f"AE Frequency {new_title}")
    plt.ylabel("$f$ (kHz)")
    plt.xlabel("r/a")
    plt.xlim([0.1,1])
    plt.ylim([0,370])
    plt.legend(loc=pos,prop={'size':9})
    plt.show()
    plt.savefig(f"All_families_plot/Frequency_{new_title}_Analysis.jpg",dpi=400)


def get_max_values(df,x):
    full_df = df.describe()
    s_max = full_df.loc["max"]
    s_min = full_df.loc["min"]
    s_max = s_max.to_frame().rename(columns={"max":f"Max_{x}"})
    s_min = s_min.to_frame().rename(columns={"min":f"Min_{x}"})
    new_df = s_max.join(s_min)
    return new_df


def plot_individual_F_analysis(df_prof,mark,new_title,dictionary,pos,x):
    if not os.path.exists(f"{x}/separated_profiles"):
        os.makedirs(f"{x}/separated_profiles")
    
    df_prof_g = df_prof.groupby(["Alfvén_mode"])
    for af,df in df_prof_g:
        ex = df_prof[df_prof["Alfvén_mode"].isin([af])]
        plt.scatter(df["radial_pos"],df["f(kHz)"],color="black",marker=mark[af],facecolors='none',alpha=2,
                    s = 60, label=new_title if af == "HAE" else None)
        plt.scatter(df["radial_pos"],df["f(kHz)"],c=ex["Growth Rate"],cmap = 'jet',marker=mark[af], s = 30)
        plt.clim(0,1)
    
    for i in range(len(dictionary['continuum'])):
        data = read_continuum(dictionary['continuum'][i])
        plt.plot(data["r"],data["freq"],"o",color=dictionary['colors'][i],markersize=1)
    
    plt.colorbar()
    plt.title(f"AE Frequency {new_title} {dictionary['title']}")
    plt.ylabel("$f$ (kHz)")
    plt.xlabel("r/a")
    plt.xlim([0.1,1])
    plt.ylim([0,370])
    plt.legend(loc=pos,prop={'size':9})
    plt.show()
    plt.savefig(f"{x}/separated_profiles/Frequency_{new_title}_Analysis_{dictionary['title']}.jpg",dpi=400)
