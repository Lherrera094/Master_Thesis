#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid

# %%


#import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# %%


#Read Alfven data
def read_dataframe(x):
    exp_df = pd.read_excel(f"n{x}/Output_Exp_{x}.xlsx")    #Experimental Profile
    
    OnA_df = pd.read_excel(f"{x}/Output_OnA_{x}.xlsx")    #On Axis Profile
    
    OfA_df = pd.read_excel(f"{x}/Output_OfA_{x}.xlsx")    #Off Axis Profile
    
    hg_df = pd.read_excel(f"{x}/Output_HG_{x}.xlsx")      #High Gradient Profile 
    
    lg_df = pd.read_excel(f"{x}/Output_LG_{x}.xlsx")      #Low Gradient Profile
    
    return exp_df,OnA_df,OfA_df,hg_df,lg_df


# %%
def read_df(x,prof):
    df = pd.read_excel(f"n{x}/Output_{prof}_n{x}.xlsx")
    df = df.drop(df[df[f"radial_pos_maximum"] > 0.8].index)
    return df


# %%


#Read Continuum
def alfv_continuum_read(x,f_max,path):
    df = pd.read_csv(f"{path}output_column_n={x}.txt", sep="\t")
    df.columns = ["r",f"n={x}"]
    df["r"] = np.sqrt(df["r"]) 
    df = df.drop(df[df[f"n={x}"] <= 10].index)
    df = df.drop(df[df[f"n={x}"] > f_max].index)
    
    color = ["white","navy","magenta","black","firebrick","blue","darkcyan",
              "darkgreen","royalblue","green","red","indigo","salmon","mediumpurple",
              "dimgrey","orange"]
    
    return df, color[x]


# %%


def family_information(fam):
    
    markers = {'HAE':"o","TAE":"^",'GAE':"s"}
    
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
    
    return markers, dictionary[fam]


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
            'y': 0.9,  # Adjust the vertical position of the title
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
    
    fig.write_image(f"{save_file}/continuum.png",width=800, height=600, scale=3)


# %%


def individual_helical_plot(df,f_max,dict_fam,path):
    title = dict_fam["title"]
    
    # plot the data
    fig = go.Figure()
    
    fig = px.scatter(df,
                     x = "radial_pos_maximum",
                     y = "f(kHz)",
                     size = "width",
                     color = "Growth Rate",
                     symbol = "Alfvén_mode",
                     hover_data=["efast","beta","dominant_mode"],
                     labels=dict(beta = "Beta_f",
                                 radial_pos_maximum="Position",
                                 dominant_mode = "Dominant Mode"))

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
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
                            )
                        )
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        title={
            'text': f"Alfvén Continuum {title}",
            'y': 1.0,  # Adjust the vertical position of the title
            'x': 0.5,  # Set the x position to center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)  # Customize the font size of the title
        }
    )
    fig.update_xaxes(title_text='r/a',title_font = {"size": 24})
    fig.update_yaxes(title_text='Frequency (kHz)',title_font = {"size": 24})
    fig.update_layout(yaxis_range=[0,300])
    fig.update_layout(xaxis_range=[0,1])
    fig.show()
    fig.write_html("Experimental profile.html")


# %%
