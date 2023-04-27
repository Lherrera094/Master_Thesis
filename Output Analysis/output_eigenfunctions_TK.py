#!/usr/bin/env python
# coding: utf-8
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
from PyPDF2 import PdfFileWriter, PdfFileReader


def create_files():
    act_dir = os.listdir()
    saving_file = "data_plots/"
    file = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))
    if not os.path.exists(saving_file):
        os.makedirs(saving_file)

    results = pd.DataFrame(columns=['beta', 'efast', 'dominant_mode', 'radial_pos',
                                    'coupling','radial_pos_2','Possible_EAE',
                                    'radial_pos_3','Alfvén_mode','Growth Rate',
                                    'Frequency','f(kHz)'])
    
    main_file = list(filter(lambda act_dir: "00_main" in act_dir, act_dir))
    main_file = os.listdir(main_file[0])
    txt = list(filter(lambda main_file: ".txt" in main_file, main_file))[0]
    
    return results,file,txt,saving_file

def remove_files(direct):
    deleted_list = ["xfar3d","fs00000","fort87","fs00001","fs00002","fs00003","fs00004",
                    "fs00005","fs00006","fs00007","fs00008","fs00009"]
    file = os.listdir(direct)
    for f in file:
        if f in deleted_list:
            os.remove(direct + "/"+f)


def plasma_parameters(directory,profiles,frec):
    in_data = open(directory + '/farprt')
    nin_data = in_data.readlines()
    data = open(directory + '/' + profiles)
    ndata = data.readlines()
    mi = 1.67e-27
    mu_0 = 1.25664e-06
    e = 1.602e-19
    
    #frecuency
    tline = [idx for idx,line in enumerate(nin_data) if 'cvfp:' in line][0] + 1
    kev = nin_data[tline].split(",")
    kev = float(kev[0])
    
    #frecuency
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


def get_main_data(f):
    data = open(f+'/farprt')
    ndata = data.readlines()
    tline = [idx for idx,line in enumerate(ndata) if 'n       Avg. gam:         Avg. om_r:' in line][0] + 1
    n, grwth, omega = ndata[tline].split()
    grwth, omega = float(grwth), float(omega)
    
    return n, grwth, omega


#Print file important data
def get_values(data_frame):
    data = data_frame.abs()
    df_desc = data.describe()
    s_max = df_desc.loc["max"]
    dominant_mode = s_max[s_max.isin([ max(df_desc.loc["max"])])].index[0]
    radial_pos = np.argmax(data[dominant_mode].values)
    sol = dominant_mode[0]
    
    #obtain second maximum in resonance
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
    m1 = n1[0].split("-") 
    m2 = n2[0].split("-") 

    n_1,n_2 = int(n1[1]),int(n2[1])
    m_1,m_2 = int(m1[1]),int(m2[1])
    
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
    
    if(n_1 != n_2):
        alfmode = "HAE"
    if(n_1 == n_2):
        if(m_1 + 1 == m_2 or m_1 - 1 == m_2):
            alfmode = "TAE/EAE"
    
    return dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3, radial_pos_3, alfmode


def get_colors(n_family):
    
    n_family = int(n_family)
    
    if n_family == 5:
        fam = [5,9,13,17]
        colfam = ["blue","green","mediumpurple","orange"]
        colors = ["navy","blue","dodgerblue", 
                  "darkgreen","forestgreen","seagreen","green",
                  "indigo","darkviolet","mediumpurple","magenta","violet",
                  "goldenrod","darkorange","orange","gold","yellow"]
    if n_family == 6:
        fam = [6,10,14]
        colfam = ["darkturquoise","red","forestgreen"]
        colors = ["darkcyan","cyan","darkturquoise", 
                  "firebrick","crimson","red","tomato",
                  "darkgreen","forestgreen","seagreen","green","limegreen"]  
        
    if n_family == 3 or n_family==7:
        fam = [3,7,11,15]
        colfam = ["k","limegreen","mediumpurple","orange"]
        colors = ["black","dimgrey","grey", 
                  "darkgreen","forestgreen","limegreen","lime",
                  "indigo","darkviolet","mediumpurple","magenta","violet",
                  "goldenrod","darkorange","orange","gold","yellow"]
        
    if n_family == 8:
        fam = [8,12,16]
        colfam = ["limegreen","mediumpurple","orange"]
        colors = ["firebrick","crimson","red","tomato",
                  "indigo","darkviolet","mediumpurple","magenta","violet",
                  "goldenrod","darkorange","orange","gold","yellow"]
    
    return fam, colfam, colors


def eigenfunction_maps(directory):
    images = []
    
    act_dir = os.listdir(directory)
    act_dir = sorted(list(act_dir))
    new_act_dirA = sorted([f.split("_")[0] for f in act_dir],reverse=True)
    new_act_dirB = [f.split("_")[1] for f in act_dir]
    act_dir = [new_act_dirA[i] + "_" + new_act_dirB[i] for i in range(len(act_dir))]
    cont = [f.split("_")[0] for f in act_dir]
    cont = cont.count(cont[0])
    
    # Loop through the directory and add the images to the list
    for filename in act_dir:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            images.append(Image.open(os.path.join(directory, filename)))
            
    # Calculate the width and height of the output image
    output_width = int(sum([image.size[0]/2 for image in images])/cont)
    output_height = int(cont*max([image.size[1]/2 for image in images]))

    # Create a new output image
    output_image = Image.new('RGB', (output_width, output_height))
    
    # Loop through the images and paste them onto the output image
    x = 0
    contador,i = 0,0
    for image in images:
        if contador == cont:
            contador = 0
            x = 0
            i += int(output_height/cont) 
        
        output_image.paste(image.resize((int(image.size[0]/2), 
                                         int(image.size[1]/2))), (x, i))
        x += int(image.size[0]/2)
        contador += 1
        
    output_image.save(directory + "Eigenfunctions_full.jpg")
