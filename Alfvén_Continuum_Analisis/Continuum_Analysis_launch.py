# Developer: Luis Carlos Herrera Quesada
# Date: 27/04/2023
# Universidad Carlos III de Madrid


from FAR3d_output_TK import *


#n = "n3"
exp_df3,OnA_df3,OfA_df3,hg_df3,lg_df3,markers,d3,fam3 = data_analysis("n3")
plot_Freq_fam(exp_df3,OnA_df3,OfA_df3,hg_df3,lg_df3,markers,d3,fam3)
plot_Freq_motion(exp_df3,OnA_df3,OfA_df3,hg_df3,lg_df3,markers,d3,fam3)
plot_individual_F_analysis(exp_df3,markers,"Experimental",d3,"upper left",fam3)
plot_individual_F_analysis(OnA_df3,markers,"On Axis",d3,"upper left",fam3)
plot_individual_F_analysis(OfA_df3,markers,"Off Axis",d3,"upper left",fam3)
plot_individual_F_analysis(lg_df3,markers,"Low Gradient",d3,"upper left",fam3)
plot_individual_F_analysis(hg_df3,markers,"High Gradient",d3,"upper left",fam3)

#n = "n5"
exp_df5,OnA_df5,OfA_df5,hg_df5,lg_df5,markers,d5,fam5 = data_analysis("n5")
plot_Freq_fam(exp_df5,OnA_df5,OfA_df5,hg_df5,lg_df5,markers,d5,fam5)
plot_Freq_motion(exp_df5,OnA_df5,OfA_df5,hg_df5,lg_df5,markers,d5,fam5)
plot_individual_F_analysis(exp_df5,markers,"Experimental",d5,"upper left",fam5)
plot_individual_F_analysis(OnA_df5,markers,"On Axis",d5,"upper left",fam5)
plot_individual_F_analysis(OfA_df5,markers,"Off Axis",d5,"upper left",fam5)
plot_individual_F_analysis(lg_df5,markers,"Low Gradient",d5,"upper left",fam5)
plot_individual_F_analysis(hg_df5,markers,"High Gradient",d5,"upper left",fam5)

#n = "n6"
exp_df6,OnA_df6,OfA_df6,hg_df6,lg_df6,markers,d6,fam6 = data_analysis("n6")
plot_Freq_fam(exp_df6,OnA_df6,OfA_df6,hg_df6,lg_df6,markers,d6,fam6)
plot_Freq_motion(exp_df6,OnA_df6,OfA_df6,hg_df6,lg_df6,markers,d6,fam6)
plot_individual_F_analysis(exp_df6,markers,"Experimental",d6,"upper left",fam6)
plot_individual_F_analysis(OnA_df6,markers,"On Axis",d6,"upper left",fam6)
plot_individual_F_analysis(OfA_df6,markers,"Off Axis",d6,"upper left",fam6)
plot_individual_F_analysis(lg_df6,markers,"Low Gradient",d6,"upper left",fam6)
plot_individual_F_analysis(hg_df6,markers,"High Gradient",d6,"upper left",fam6)

#n = "n8"
exp_df8,OnA_df8,OfA_df8,hg_df8,lg_df8,markers,d8,fam8 = data_analysis("n8")
plot_Freq_fam(exp_df8,OnA_df8,OfA_df6,hg_df8,lg_df8,markers,d8,fam8)
plot_Freq_motion(exp_df8,OnA_df8,OfA_df6,hg_df8,lg_df8,markers,d8,fam8)
plot_individual_F_analysis(exp_df6,markers,"Experimental",d6,"upper left",fam6)
plot_individual_F_analysis(OnA_df6,markers,"On Axis",d6,"upper left",fam6)
plot_individual_F_analysis(OfA_df6,markers,"Off Axis",d6,"upper left",fam6)
plot_individual_F_analysis(lg_df6,markers,"Low Gradient",d6,"upper left",fam6)
plot_individual_F_analysis(hg_df6,markers,"High Gradient",d6,"upper left",fam6)

#Frequency by profile
d = {"continuum": np.arange(3,16),
     "colors": ["navy","magenta","k","firebrick","blue","darkcyan","darkgreen",
                "brown","green","red","indigo","salmon","mediumpurple","dimgrey",
                "orange","deepskyblue","goldenrod"]}

plot_profile_F_analysis(exp_df3,exp_df5,exp_df6,exp_df8,markers,"Experimental Profile",d,"upper left")
plot_profile_F_analysis(OnA_df3,OnA_df5,OnA_df6,OnA_df8,markers,"On-Axis Profile",d,"upper center")
plot_profile_F_analysis(OfA_df3,OfA_df5,OfA_df6,OfA_df8,markers,"Off-Axis Profile",d,"upper left")
plot_profile_F_analysis(lg_df3,lg_df5,lg_df6,lg_df8,markers,"Low-Gradient Profile",d,"upper left")
plot_profile_F_analysis(hg_df3,hg_df5,hg_df6,hg_df8,markers,"High-Gradient Profile",d,"upper center")
