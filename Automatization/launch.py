#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys 
sys.path.append('FAR3_libraries/')
from launch_simulations import *


# In[2]:


launch_num = 8 #number of simulations to launch

act_dir = os.listdir()
files = sorted(list(filter(lambda act_dir: "efast" in act_dir, act_dir)))

done = launch_sims(files,launch_num)


# In[ ]:





# In[ ]:




