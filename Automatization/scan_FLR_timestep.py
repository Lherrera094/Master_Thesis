import pandas as pd
import numpy as np
import os, sys, subprocess

source_folder      =  os.path.abspath("./00_main_input")

# +
main_file = os.listdir(source_folder)
equilibrium = list(filter(lambda main_file: "Eq_" in main_file, main_file))[0]
text = list(filter(lambda main_file: ".txt" in main_file, main_file))[0]
sh = list(filter(lambda main_file: ".sh" in main_file, main_file))[0]

source_input_model = f"{source_folder}/Input_Model"
source_input_eq    = f"{source_folder}/"+equilibrium
source_input_profs = f"{source_folder}/"+text
source_exec        = f"{source_folder}/xfar3d"
source_run         = f"{source_folder}/"+sh
# -

folderfile        =   os.path.abspath("./tfolders.txt")

cwd               = os.getcwd()

with open(folderfile, 'r') as tfile:
    foldernames = tfile.readlines()

# results = pd.DataFrame(columns=['beta', 'efast', 'n', 'grwth', 'omega'])
k = 0
for folder in foldernames:
    x = folder.split('\t')
    
    if len(x) == 5:
        beta, tfast, omegar, r_epflr, timestep = folder.split()   
    else:
        beta, tfast, omegar, timestep = folder.split()
        
    tfoldername     = f"efast_{tfast}_beta_{beta}"
    out_input_model = os.path.abspath(f"./{tfoldername}/Input_Model")
    
    ## Make folder, copy Input_Model
    subprocess.run(["mkdir", "-p", tfoldername])
    subprocess.run(["cp", source_input_model, out_input_model])
    
    ## Linking other files
    subprocess.run(["ln", "-sf", source_input_eq,    f"{tfoldername}/"+equilibrium])
    subprocess.run(["ln", "-sf", source_input_profs, f"{tfoldername}/"+text])
    subprocess.run(["ln", "-sf", source_exec,        f"{tfoldername}/xfar3d"])
    subprocess.run(["ln", "-sf", source_run,         f"{tfoldername}/"+sh])
    
    ## Change executable
    with open(out_input_model, 'r') as tfile:
        ndata    = tfile.readlines()
        
    ## Change beta
    tline        = [idx for idx,line in enumerate(ndata) if 'bet0_f: ' in line][0] + 1
    ndata[tline] = f"{beta}\n"
    
    ## Change omegar
    tline        = [idx for idx,line in enumerate(ndata) if 'omegar: ' in line][0] + 1
    ndata[tline] = f"{omegar}\n"
    
    if len(x) == 5:
        ## Change r_epflr
        tline        = [idx for idx,line in enumerate(ndata) if 'r_epflr: ' in line][0] + 1
        ndata[tline] = f"{r_epflr}\n"
    
    ## Change timestep
    tline        = [idx for idx,line in enumerate(ndata) if 'maxstp: simulation time steps ' in line][0] + 1
    ndata[tline] = f"{timestep}\n"
    
    ## Change cvfp
    cvfp         = tfast 
    tline        = [idx for idx,line in enumerate(ndata) if 'cvfp: ' in line][0] + 1
    ndata[tline] = f"{cvfp}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0\n"
    
    with open(out_input_model, 'w') as nfile:
        nfile.writelines(ndata)
    ## Run bash file
    os.chdir(tfoldername)
    # subprocess.Popen("./TJII.sh")
    os.chdir(cwd)
    #farprt = f"{folder}/temp_grwth_omega"



