#!/usr/bin/env python
# coding: utf-8

# In[1]:


from output_eigenfunctions_TK import *


# In[2]:


#Loop to read all files from pathhhh
l = 0
results, files, txt,saving_file = create_files()

for file in files:
    try:
        #read data
        df = pd.read_csv(file + "/phi_0000", sep="\t")
        r = df["r"]
        df = df.drop("r",axis=1)
    
        #Get data analysis 
        n_family, gr, freq = get_main_data(file)
        dominant_mode, radial_pos, dominant_mode_2, radial_pos_2,dominant_mode_3,radial_pos_3, alfmode = get_values(df)
        family, colfam, colors = get_colors(n_family)
        frequency, energy, beta, kev = plasma_parameters(file,txt,abs(freq))
    
        #save data in dataframe
        results.loc[l] = [beta, round(energy), dominant_mode, radial_pos/1000, dominant_mode_2, 
                      radial_pos_2/1000,dominant_mode_3,radial_pos_3, alfmode,
                          gr,freq,frequency]
        l += 1
        remove_files(file)
        
        #plot phi
        exist = os.path.isfile("data_plots/"+str(round(energy)) +"_"+ str(beta) +".jpg")
        if exist == False:
            clear_output(wait=True)
            im = plt.figure(figsize=(9,8))
            i,j,k=0,0,0

            plt.annotate('Dominant Mode: ' + dominant_mode, xy=(0.01, 0.335), 
                         xycoords='axes fraction', fontsize = 15)
            plt.annotate('Coupled: ' + dominant_mode_2, xy=(0.01, 0.305), 
                         xycoords='axes fraction', fontsize = 15)
            plt.annotate('Alfvén Mode: ' + alfmode, xy=(0.01, 0.275), 
                         xycoords='axes fraction', fontsize = 15)
        
            if(int(n_family[0])==6):
                plt.axvline(radial_pos_2/1000,color="k",linewidth=1)
                plt.axvline(radial_pos/1000,color="blue",linewidth=1)
            
            else:
                plt.axvline(radial_pos_2/1000,color="k",linewidth=1)
                plt.axvline(radial_pos/1000,color="red",linewidth=1)
            
            if radial_pos_3 != "--":
                plt.axvline(radial_pos_3/1000,color="k",linestyle="--",linewidth=1)
                plt.annotate('2nd Coupled: ' + dominant_mode_3, xy=(0.01, 0.245), 
                             xycoords='axes fraction', fontsize = 15)

            for n in family:
                plt.axhline(0,xmin = 0.05, xmax = 0.07,color=colfam[k],linewidth=2,
                            label="n= " + str(n))
                k += 1
    
            for col in df.columns:
                if "I" in col:
                    plt.plot(r,df[col],"--",color=colors[i],linewidth=1.5)
                    i += 1
                if "R" in col:
                    plt.plot(r,df[col],color=colors[j],linewidth=1.5)
                    j+=1
        
            plt.title("EP "+str(round(energy)) +"keV/"+r"$\beta$: " + str(beta) + "/f: "+ str(round(frequency))+" kHz",
                      fontsize=22)   
            plt.xlabel("r/a",fontsize=20)
            plt.ylabel("$\Phi$",fontsize=20)
            plt.grid(True)
            plt.legend(loc="lower left")
            plt.savefig("data_plots/"+ str(round(energy)) +"_"+ str(beta) +".jpg",dpi=600)
            plt.close('all')    
        
    except Exception as e:
        print(e)
        
results.to_excel('results.xlsx')
eigenfunction_maps(saving_file)


# In[ ]:




