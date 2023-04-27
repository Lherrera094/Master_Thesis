#!/usr/bin/env python
# coding: utf-8
# %%
# Developer: Luis Carlos Herrera Quesada
# Date: 28/03/2023
# Universidad Carlos III de Madrid
# %%
import os 
import subprocess

launch_num = 8 #number of simulations to launch
count = 0

act_dir = os.listdir()
files = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))

def run_files(entry,sim):
	print(sim+":")
	subprocess.call("qsub "+entry, shell = True,cwd=sim+"/")
	
for i in range(len(files)):
	file = os.listdir(files[i])
	bash = list(filter(lambda file: ".sh" in file, file))[0]
	if "farprt" not in file and count < launch_num:
		run_files(bash,files[i])
		count += 1
