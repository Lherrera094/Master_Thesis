
# Developer: Luis Carlos Herrera Quesada
# Date: 28/04/2023
# Universidad Carlos III de Madrid

from Resonant_modes_TK import *

#Initial Variables and sets
iota = ["Experimental/","iota_1.3/","iota_1.5/","iota_1.9/","iota_2.1/"]
pos = ["upper left","center left","lower left","lower right"]
size = 9
periods = 4
i = iota[2]

#call of functions
iota_df = read_data_iota(i)
i_M,i_m,couplings = resonance_coupling(iota_df)
couplings.to_excel(f"{i}/Full_coupling_list.xlsx",index=False)
plot_iota(iota_df,i)
plot_resonant_modes(couplings,periods,i,pos[2],iota_df,size)

plot_all_iota(iota)
