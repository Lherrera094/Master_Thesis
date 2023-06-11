#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 31/05/2023
# Universidad Carlos III de Madrid

# %%
#import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import webbrowser
from pathlib import Path
import os


# %%
def read_df(x,prof,fam):
    
    nomb = "."
    dir_image = f"{fam}/Eigenfunction_plots/"
    image = os.listdir(dir_image)
    localh = f"<a href=\"http://localhost:8888/view/Documents/Master/TFM/Data_Analysis/1_Experimental_Profile/{dir_image}"
    local_host_image = [] 
    
    image = sorted(image, key=lambda x: (float(x.split('_')[0]), float(x.split('_')[1].split('.png')[0])))
    
    for i in image:
        local_host_image.append(f"{localh}{i}\">{nomb}</a>")
    
    link_df = pd.DataFrame(local_host_image, columns=["link_to_image"])
    
    df = pd.read_excel(f"n{x}/Output_{prof}_n{x}.xlsx")
    #df["radial_pos_maximum"] = np.sqrt(df["radial_pos_maximum"])
    df["link_to_image"] = link_df
    df = df.drop(df[df[f"radial_pos_maximum"] > 0.8].index)
    
    return df


# %%


#Read Continuum
def alfv_continuum_read(x,f_max,path):
    df = pd.read_csv(f"{path}output_column_n={x}.txt", sep="\t")
    df.columns = ["r",f"n={x}"]
    df["r"] = np.sqrt(df["r"]) 
    df = df.drop(df[df[f"n={x}"] <= 5].index)
    df = df.drop(df[df[f"n={x}"] > f_max].index)
    
    color = ["white","black","navy","darkslategrey","sandybrown","blue","darkturquoise",
              "forestgreen","springgreen","darkred","orange","darkmagenta","olive",
             "grey","red","dodgerblue","mediumvioletred","forestgreen"]
    
    return df, color[x]


# %%


def family_information(fam):
    
    dictionary = {
        "n7": {
            "title": "n=7,11,15",
            "continuum": [7,11,15],
            "colors": ["green","indigo","orange"],
            "ylim_f":[0,300],
            "ylim_gr":[0,1],
            "position":"upper left"
        },
        "n5": {
            "title": "n=5,9,13,17",
            "continuum": [5,9,13],
            "colors": ["green","mediumpurple","goldenrod"],
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
    
    return dictionary[fam]


# %%
# ## Alfvén Continuum

def alfv_continuum(f_max,save_file,path):
    # plot the data
    fig = go.Figure()

    for i in range(1,16):
        df,colors = alfv_continuum_read(i,f_max,path)
        fig = fig.add_trace(go.Scatter(x = df["r"],
                                       y = df[f"n={i}"], 
                                       mode='markers',
                                       marker=dict(
                                        size=3,
                                        color=colors   
                                        ),
                                       name = f"n={i}"))

    fig.update_layout(
        title={
            'text': "Alfvén Continuum",
            'y': 0.95,  # Adjust the vertical position of the title
            'x': 0.5,  # Set the x position to center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)  # Customize the font size of the title
        }
    )
    fig.update_xaxes(title_text='r/a',title_font = {"size": 20})
    fig.update_yaxes(title_text='Frequency (kHz)',title_font = {"size": 20})
    fig.update_layout(yaxis_range=[0,f_max])    
    fig.show()
    
    fig.write_html(f"{save_file}/Continuum_html.html")
    fig.write_image(f"{save_file}/continuum.png",width=800, height=600, scale=3)


# %%
def individual_helical_plot(df,f_max,dict_fam,path,save_file,fam,image_path):
    
    title = dict_fam["title"]
    fig = go.Figure()
    
    fig = px.scatter(df,
                     x = "radial_pos_maximum",
                     y = "f(kHz)",
                     text = df["link_to_image"],
                     size = "width",
                     color = "Growth Rate",
                     symbol = "Alfvén_mode",
                     hover_data=["efast","beta","dominant_mode"],
                     labels=dict(beta = "Beta_f",
                                 radial_pos_maximum="Position",
                                 dominant_mode = "Dominant Mode"))
    
    fig.update_traces(textposition = "middle center")
    fig.update_layout(uniformtext_minsize=4, uniformtext_mode='hide')
    
    for i in dict_fam["continuum"]:
        df_cont,colors = alfv_continuum_read(i,f_max,path)
        fig = fig.add_trace(go.Scatter(x = df_cont["r"],
                                       y = df_cont[f"n={i}"], 
                                       mode='markers',
                                        marker=dict(
                                        size=3,
                                        color=colors   
                                        ),
                                        name = f"n={i}"))
    
    fig.update_layout(
                hoverlabel=dict(
                bgcolor="bisque",
                font_size=14,
                font_family="Rockwell"
                            )
                        )
    
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        title={
            'text': f"Alfvén Continuum {title}",
            'y': 0.95,  # Adjust the vertical position of the title
            'x': 0.5,  # Set the x position to center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)  # Customize the font size of the title
        },
        font=dict(size=15),
    )
    
    fig.update_xaxes(title_text='r/a',title_font = {"size": 24})
    fig.update_yaxes(title_text='Frequency (kHz)',title_font = {"size": 24})
    fig.update_layout(yaxis_range=[0,300])
    fig.update_layout(xaxis_range=[0.1,1])
    
    fig.show()
    fig.write_image(f"{save_file}/{title}_Contiuum.png",width=800, height=600, scale=3)
    fig.write_html(f"{save_file}/Experimental_profile_{title}.html")


# %%
def maximum_instability_energy(df5,df6,df7):
    
    E_ep_n5, beta_n5, gr5 = get_max_gr(df5)
    E_ep_n6, beta_n6, gr6 = get_max_gr(df6)
    E_ep_n7, beta_n7, gr7 = get_max_gr(df7)
    
    max_gr = [gr5,gr6,gr7]
    
    maximum = check_max_value(max_gr)
    
    if maximum == gr5:
        gr = gr5
        beta = beta_n5
        E_ep_h = E_ep_n5
        fam = "n = 5,9,13,17"
    
    elif maximum == gr6:
        gr = gr6
        beta = beta_n6
        E_ep_h = E_ep_n6
        fam = "n = 6,10,14"
    
    else:
        gr = gr7
        beta = beta_n7
        E_ep_h = E_ep_n7
        fam = "n=7,11,15"
    
    df_new_n5 = df5.drop(df5[df5['efast'] != E_ep_h].index)
    df_new_n6 = df6.drop(df6[df6['efast'] != E_ep_h].index)
    df_new_n7 = df7.drop(df7[df7['efast'] != E_ep_h].index)
    
    return df_new_n5, df_new_n6, df_new_n7, E_ep_h, gr, beta, fam


# %%
def get_max_gr(df):
    #Gets row for the simulation with larger growth rate
    gr_index = df[df["Growth Rate"] == df["Growth Rate"].max()].index
    
    gr = df.loc[gr_index]["Growth Rate"].values[0]
    E_ep = df.loc[gr_index]["efast"].values[0]
    beta = df.loc[gr_index]["beta"].values[0]
    
    return E_ep, beta, gr


# %%
def check_max_value(n_array):
    
    maximum = n_array[0]  # Initialize the maximum as the first element
    
    for num in n_array:
        if num > maximum:
            maximum = num
            
    return maximum


# %%
def maximum_instability_beta(df5,df6,df7):
    
    E_ep_n5, beta_n5, gr5 = get_max_gr(df5)
    E_ep_n6, beta_n6, gr6 = get_max_gr(df6)
    E_ep_n7, beta_n7, gr7 = get_max_gr(df7)
    
    max_gr = [gr5,gr6,gr7]
    
    maximum = check_max_value(max_gr)
    
    if maximum == gr5:
        gr = gr5
        beta = beta_n5
        E_ep_h = E_ep_n5
        fam = "n = 5,9,13,17"
    
    elif maximum == gr6:
        gr = gr6
        beta = beta_n6
        E_ep_h = E_ep_n6
        fam = "n = 6,10,14"
    
    else:
        gr = gr7
        beta = beta_n7
        E_ep_h = E_ep_n7
        fam = "n=7,11,15"
    
    df_new_n5 = df5.drop(df5[df5['beta'] != beta].index)
    df_new_n6 = df6.drop(df6[df6['beta'] != beta].index)
    df_new_n7 = df7.drop(df7[df7['beta'] != beta].index)
    
    return df_new_n5, df_new_n6, df_new_n7, E_ep_h, gr, beta, fam
