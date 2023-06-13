#!/usr/bin/env python
# coding: utf-8
# %%
import booz_xform as bx
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np


# %%
def vmec_to_Boozer(vmec_file,save_file,device,profile,surfaces):
    b = bx.Booz_xform()
    b.read_wout(f"{vmec_file}")
    b.compute_surfs = surfaces
    b.run()
    b.write_boozmn(f"{save_file}/boozmn_{device}_{profile}.nc")

    return b


# %%
def plot_iota(b,save_file,profile):
    x = [0,0.2,0.4,0.6,0.8,1.0]
    iota = abs(b.iota)
    r = np.sqrt(np.linspace(0,1,len(iota)))
    
    plt.plot(r,iota,color="darkcyan")
    plt.title("Rotational Transform",fontsize=30)
    plt.xlabel("r/a",fontsize = 27)
    plt.ylabel(r"$\iota$(r)",fontsize = 27)
    plt.xticks(x)
    plt.grid(True)
    plt.show()
    plt.savefig(f"{save_file}/Iota_{profile}.png",dpi = 400)


# %%
def B_plot(b,surface,save_file):
    
    x_label = [0,r"$\pi$/8",r"$\pi$/4",r"3$\pi$/8",r"$\pi$/2"]
    x = [0,0.393,0.7853,1.178,1.57] 
    y_label = [0,r"$\pi$/2",r"$\pi$",r"$3\pi$/2",r"$2\pi$"]
    y = [0,1.57,3.1415,4.712,6.283] 
    
    figure = bx.surfplot(b,js=surface,cmap=plt.cm.jet)
    plt.title(r"$|B|$ on s = " + f"{surface}")
    plt.xlabel(r"Toroidal Angle $\varphi_B$")
    plt.ylabel(r"Poloidal Angle $\theta_B$")
    plt.xticks(x,x_label)
    plt.yticks(y,y_label)
    plt.savefig(f"{save_file}/Heatmap_B_{surface}.png",dpi = 400)
    plt.show(figure)


# %%
def select_file():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    
    return file

