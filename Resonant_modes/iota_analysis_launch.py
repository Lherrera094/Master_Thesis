#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 28/04/2023
# Universidad Carlos III de Madrid

# %%


from iota_Analysis_TK import *


# %%


#Initial Variables and sets
iota = ["Experimental/","iota_1.3/","iota_1.5/","iota_1.9/","iota_2.1/"]
pos = ["upper left","center left","lower left","lower right"]
equil_modes = [0,4,8,12,16]
size = 10
periods = 4
error = 0
i = iota[4]

i = i.split("/")[0]

#define reference profile
ref_iota = read_data_iota(iota[0])
reference_i = iota_max = max(abs(ref_iota["       iota"]))

#call of functions
iota_df = read_data_iota(i)
i_M,i_m,couplings = resonance_coupling(iota_df,error)
couplings.to_excel(f"{i}/Full_coupling_list.xlsx",index=False)
plot_iota(iota_df,i)
plot_coupling_modes(couplings,periods,i,pos[2],iota_df,size,reference_i)
plot_resonant_modes(couplings,periods,i,iota_df,reference_i)


# %%

plot_all_iota(iota)

