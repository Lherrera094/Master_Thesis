#!/usr/bin/env python
# coding: utf-8
# +
# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid
# -

import pandas as pd
import matplotlib.pyplot as plt
import os 
import numpy as np
from ipywidgets import interact, interactive, fixed
from IPython.display import clear_output
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from PIL import Image
import os


#Read all folders and create the folder to save the plots
def create_files():
    act_dir = os.listdir()
    saving_file = "Eigenfunction_plots/"
    file = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))
    if not os.path.exists(saving_file):
        os.makedirs(saving_file)

    results = pd.DataFrame(columns=['beta', 'efast', 'dominant_mode', 'radial_pos_maximum','width_i','width_f',
                                    'width','coupling','radial_pos_2','Possible_EAE',
                                    'radial_pos_3','Alfvén_mode','Growth Rate',
                                    'Frequency','f(kHz)'])
    
    main_file = list(filter(lambda act_dir: "00_main" in act_dir, act_dir))
    main_file = os.listdir(main_file[0])
    txt = list(filter(lambda main_file: ".txt" in main_file, main_file))[0]
    
    return results,file,txt,saving_file

def sort_key(item):
    parts = item.split('.png')
    first, last = parts[0].split('_')
    return float(first), -float(last)


#Remove not used files for each folder
def remove_files(direct):
    deleted_list = ["xfar3d","fs00000","fort87","fs00001","fs00002","fs00003","fs00004",
                    "fs00005","fs00006","fs00007","fs00008","fs00009"]
    file = os.listdir(direct)
    for f in file:
        if f in deleted_list:
            os.remove(direct + "/"+f)


#From farprt and profiles.dat obtains the relevant plasma characteristics
def plasma_parameters(directory,profiles,frec):
    in_data = open(directory + '/farprt')
    nin_data = in_data.readlines()
    data = open(directory + '/' + profiles)
    ndata = data.readlines()
    mi = 1.67e-27
    mu_0 = 1.25664e-06
    e = 1.602e-19
    
    #EP energy
    tline = [idx for idx,line in enumerate(nin_data) if 'cvfp:' in line][0] + 1
    kev = nin_data[tline].split(",")
    kev = float(kev[0])
    
    #EP beta
    tline = [idx for idx,line in enumerate(nin_data) if 'bet0_f' in line][0] + 1
    beta = nin_data[tline].split("\t")
    beta = float(beta[0])
    
    #Magnetic Field
    tline = [idx for idx,line in enumerate(ndata) if 'Vacuum' in line][0] + 1
    B = ndata[tline].split("\t")
    B = B[1].split("\n")
    B = float(B[0])
    
    #Major Radius
    tline = [idx for idx,line in enumerate(ndata) if 'Geometric Center' in line][0] + 1
    R = ndata[tline].split("\t")
    R = R[1].split("\n")
    R = float(R[0])
    
    #Main Ion species mass/proton
    tline = [idx for idx,line in enumerate(ndata) if 'Main Ion' in line][0] + 1
    M = ndata[tline].split("\t")
    M = M[0].split(" ")
    M = float(M[4])
    
    #Density and safety factor
    tline = [idx for idx,line in enumerate(ndata) if 'Rho' in line][0] + 1
    full_line = ndata[tline].split("\t")
    full_line = full_line[0].split(" ")
    q = float(full_line[1])
    ni = float(full_line[3])
    ni = ni*10**(20)
    
    #Alfvén speed
    Va = (B)/np.sqrt(M*mu_0*mi*ni)

    #Frecuency
    f = (frec*Va)/(2*np.pi*R*1000*q)
    #Energy
    energy = mi*(kev*Va)**2/(e*1000)
    
    return f, energy, beta, kev


#From farprt obtains frequency and growth rate
def get_main_data(f):
    data = open(f+'/farprt')
    ndata = data.readlines()
    line_diference = 4
    toroidal_couplings = []
    
    tline = [idx for idx,line in enumerate(ndata) if 'n       Avg. gam:         Avg. om_r:' in line][0] + 1
    n, grwth, omega = ndata[tline].split()
    toroidal_couplings.append(n)

    if grwth == "NaN":
        grwth, omega = 0,-1000
    else: 
        grwth, omega = float(grwth), float(omega)
    try:
        for i in range(1,10):
            tline = [idx for idx,line in enumerate(ndata) if 'n       Avg. gam:         Avg. om_r:' in line][0] + 1 + (line_diference*i)
            n, grwth1, omega1 = ndata[tline].split()
            toroidal_couplings.append(n)
        
            if grwth1 == "NaN" or grwth1 == "nan":
                grwth1, omega1 = 0,-1000
            else:
                grwth1, omega1 = float(grwth1), float(omega1)
                
            if grwth1 >= grwth:
                grwth = grwth1
                omega = omega1

    except Exception as e:
        x = 0

    return grwth, omega, toroidal_couplings


#Print file important data
def get_values(data_frame):
    #Obtain Eigenmode with maximum amplitude
    data = data_frame.abs()
    df_desc = data.describe()
    s_max = df_desc.loc["max"]
    
    #Column name for the mode with maximum amplitude
    dominant_mode = s_max[s_max.isin([max(df_desc.loc["max"])])].index[0] 
    radial_pos = np.argmax(data[dominant_mode].values)
    sol = dominant_mode[0]

    #Width of the maximum mode
    max_df = data_frame[dominant_mode]
    y1,x1,y2,x2,width = dominant_mode_width(max_df)
    
    #Delete dominant mode from data_frame
    data = data.drop(dominant_mode,axis=1)
    for col in data.columns:
        if sol not in col:
            data = data.drop(col,axis=1)
       
    #treshold = 1
    #while(treshold <= 0.08):
    df_desc_sec = data.describe()
    s_max = df_desc_sec.loc["max"]
    dominant_mode_2 = s_max[s_max.isin([ max(df_desc_sec.loc["max"])])].index[0]
    radial_pos_2 = np.argmax(data[dominant_mode_2].values)
    treshold = abs(radial_pos - radial_pos_2)/1000
    data = data.drop(dominant_mode_2,axis=1)  
    
    n1 = dominant_mode.split("/")
    n2 = dominant_mode_2.split("/")
    
    try:
        m1 = n1[0].split("-") 
        m2 = n2[0].split("-")
        m_1,m_2 = int(m1[-1]),int(m2[-1])

    except Exception as e: 
        m1 = n1[0].split(" ") 
        m2 = n2[0].split(" ")
        m_1,m_2 = int(m1[-1]),int(m2[-1])

    n_1,n_2 = int(n1[1]),int(n2[1])
    
    try:
        if(n_1 == n_2):
            df_desc_3 = data.describe()
            s_max = df_desc_3.loc["max"]
            dominant_mode_3 = s_max[s_max.isin([ max(df_desc_3.loc["max"])])].index[0]
            radial_pos_3 = np.argmax(data[dominant_mode_3].values)
            treshold = abs(radial_pos - radial_pos_3)/1000
            data = data.drop(dominant_mode_3,axis=1)
        else:
            dominant_mode_3 = "--"
            radial_pos_3 = "--"
    except Exception as e:
        dominant_mode_3 = "--"
        radial_pos_3 = "--"
    
    if(n_1 != n_2):
        alfmode = "HAE"
    if(n_1 == n_2):
        if(m_1 + 1 == m_2 or m_1 - 1 == m_2):
            alfmode = "TAE/EAE"
    
    return dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3, radial_pos_3, alfmode, x1, x2, width


def get_colors_dict(n):
    n = int(n)
    
    d =  {
	1: {
            'colfam': "mediumpurple",
            'colors': ["indigo","darkviolet","mediumpurple","magenta","violet"] 
        },
	2: {
            'colfam': 'darkturquoise',
            'colors': ['darkcyan', 'cyan', 'darkturquoise','mediumturquoise','turquoise']             
        },
        3: {
            'colfam': 'k',
            'colors': ['black', 'dimgrey', 'grey','silver','lightgrey']             
        },
	4: {
            'colfam': "orange",
            'colors': ["goldenrod","darkorange","orange","gold","yellow"] 
        },
        
        5: {
            'colfam': 'blue',
            'colors': ['navy', "steelblue",'blue', 'dodgerblue','lightskyblue']
        },
        6: {
            'colfam': 'darkturquoise',
            'colors': ['darkcyan', 'cyan', 'darkturquoise','mediumturquoise','turquoise']
        },
        
        7: {
            'colfam': 'limegreen',
            'colors': ['darkgreen', 'forestgreen', 'limegreen', 'lime','green']
        },
        8: {
            'colfam': 'red',
            'colors': ['firebrick', 'crimson', 'red', 'tomato','salmon']
        },
        9: {
            'colfam': "green",
            'colors': ["darkgreen","forestgreen","seagreen","green","limegreen"] 
        },
        10: {
            'colfam': "red",
            'colors': ["firebrick","crimson","red","tomato",'salmon'] 
        },
        11: {
            'colfam': "mediumpurple",
            'colors': ["indigo","darkviolet","mediumpurple","magenta","violet"] 
        },
        12: {
            'colfam': 'k',
            'colors': ['black', 'dimgrey', 'grey','silver','lightgrey']  
        },
        13: {
            'colfam': "mediumpurple",
            'colors': ["indigo","darkviolet","mediumpurple","magenta","violet"] 
        },
        14: {
            'colfam': "forestgreen",
            'colors': ["darkgreen","forestgreen","seagreen","green","limegreen"] 
        },
        15: {
            'colfam': "orange",
            'colors': ["goldenrod","darkorange","orange","gold","yellow"] 
        },
        16: {
            'colfam': 'blue',
            'colors': ['navy', "steelblue",'blue', 'dodgerblue','lightskyblue']
        },
        17: {
            'colfam': "orange",
            'colors': ["goldenrod","darkorange","orange","gold","yellow"] 
        },
    }
    
    return d[n]


def plot_eigenfunctions(dm,dm2,dm3,alfm,rp,rp2,rp3,df,r,energy,beta,f,sav_file,tor_coupl):
    im = plt.figure(figsize=(9,8))
    i,j,k=0,0,0
    
    #Information about the dominant modes
    plt.annotate(f"Dominant Mode: {dm}", xy=(0.01, 0.335), xycoords='axes fraction', fontsize = 15)    
    plt.annotate(f"Coupled: {dm2}", xy=(0.01, 0.305), xycoords='axes fraction', fontsize = 15)             
    plt.annotate(f"Alfvén Mode: {alfm}", xy=(0.01, 0.275), xycoords='axes fraction', fontsize = 15)
    
    #Marking lines and annotations    
    if 6 in tor_coupl:
        plt.axvline(rp/1000,color="blue",linewidth=1)
            
    else:
        plt.axvline(rp/1000,color="red",linewidth=1)
            
    if rp3 != "--":
        plt.axvline(rp3/1000,color="k",linestyle="--",linewidth=1)
        plt.annotate(f"2nd Coupled: {dm3}", xy=(0.01, 0.245), xycoords='axes fraction', fontsize = 15)                 
    
    for n in tor_coupl:
        d = get_colors_dict(n)
        plt.axhline(0,xmin = 0.05, xmax = 0.06,color=d["colfam"],linewidth=2,label=f"n= {n}")                   
        k += 1
                
    plt.axvline(rp2/1000,color="k",linewidth=1)
    
    #plot Eigenfunctions
    for m in tor_coupl:
        i,j=0,0
        d = get_colors_dict(m)
       
        for col in df.columns:
            if f"/ {m}" in col or f"/{m}" in col:
                if "I" in col:
                    plt.plot(r,df[col],"--",color=d['colors'][i],linewidth=1.5)
                    i += 1
                if "R" in col:
                    plt.plot(r,df[col],color=d['colors'][j],linewidth=1.5)
                    j += 1
       
    plt.title(f"EP {round(energy)} keV/ "+ r"$\beta$:"+f"{beta}/ $f$: {round(f)} kHz",fontsize=22)               
    plt.xlabel("r/a",fontsize=20)
    plt.ylabel(r"$\Phi$",fontsize=20)
    plt.grid(True)
    plt.legend(loc="lower left")
    plt.savefig(f"{sav_file}{round(energy)}_{beta}.png",dpi=200)


#Creates an array of sorted plots for panoramic visualization
def eigenfunction_maps(directory):
    images = []
    
    #Arrange list in descending order for energy and ascending for beta
    act_dir = sorted(os.listdir(directory)) #makes a list of the images names 
    act_dir = sorted(act_dir, key=sort_key,reverse=True)
         
    #Gets the number of energy plots for the array of images
    my_list = [f.split("_")[0] for f in act_dir]
    unique_elements = sorted(set(my_list),reverse=True)
    columns = []
    for element in unique_elements:
        count = my_list.count(element)
        columns.append(count)
        
    column_num = max(columns)
    row_num = len(columns)
    
    # Loop through the directory and add the images to a list
    for filename in act_dir:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            images.append(Image.open(os.path.join(directory, filename)))
            
    # Calculate the width and height of the output image
    output_width = int(column_num*(images[0].size[0]/2))
    output_height = int(row_num*(images[0].size[1]/2))

    #Create a new image
    output_image = Image.new('RGB', (output_width, output_height))
    
    # Loop through the images and paste them onto the output image
    row_count,column_count = 0,0
    num_col = 0
    x,i = 0,0 #x:image position for each column,i:image position for each column
    
    for image in images:
        if column_count == columns[num_col]:
            num_col += 1
            column_count = 0
            x = 0
            i += int(output_height/row_num) 
        
        output_image.paste(image.resize((int(image.size[0]/2), 
                                         int(image.size[1]/2))), (x, i))
        x += int(image.size[0]/2)  #Position in x for the image
        column_count += 1    
        
    output_image.save("Eigenfunctions_full.jpg")


def dominant_mode_width(max_dataframe):
    max_dataframe = pd.DataFrame(max_dataframe)
    #Defines radius column and add it to the dataframe
    radius = np.linspace(0,1000,1001)
    max_dataframe['Radius'] = radius
    max_mode = abs(max_dataframe)
    name_column = max_dataframe.columns
    
    max_mode = max_mode.loc[max_mode[name_column[0]] >= max(max_mode[name_column[0]])/2]
    
    #Obtain the points for the width for the max eigenfunction
    x1 = max_mode["Radius"].iloc[0]
    y1 = max_mode[name_column[0]].iloc[0]
    
    x2 = max_mode["Radius"].iloc[-1]
    y2 = max_mode[name_column[0]].iloc[-1]

    width = x2-x1
    
    return y1,x1,y2,x2,width
