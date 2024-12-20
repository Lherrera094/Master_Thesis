<h3 align="center"> Theoretical Study of Alfvénic Stability Optimization for TJ-II Stellarator </h3> 

From February 1st to June 27th, 2023.

Supervisor: [Jacobo Varela](https://www.researchgate.net/profile/Jacobo-Varela)

**Description**: The objective is to study the Alfvén Eigenmodes activity on the TJ-II Stellarator concerning the operation of the NBI heating system and magnetic topology variation for optimization. The analysis is performed using the linear version of the gyro-fluid code FAR3d. The Alfvén Continuum is computed with the STELLGAP code. The AE stability analysis is performed
for the n = 7,11, 15, n = 5,9,13, 17, n = 6,10,14 helical families including EP populations with energies in the range of 10 - 50 keV and EP beta from 0.1 to
0.4.


The codes developed to optimize the analysis of the [FAR3d](https://e-archivo.uc3m.es/bitstream/handle/10016/34630/Noninear_NF_2021.pdf?sequence=1) results are:

* **Automatization**: Python scripts for faster preparation of launching folder for FAR3d simulations. Scripts developed to launch simulations in cluster URANUS at Universidad Carlos III de Madrid.

* **Rotational Transform Couplings**: Code obtains the resonant modes for a rotational transform profile. It returns a plot of the resonant modes in the $\iota$ profile, and also an Excel with all relevant values. As inputs, it can receive the extremum values, the VMEC wout file or the profile.dat from FAR3d, the periods of the device (in the case of stellarators) and the equilibrium modes. 

<p align="center">
  
![Couplings](/Resonant_modes/Examples/delta_iota_0.15_Resonant.png "Example for a 4 period stellarator with high shear.")
  
</p>

* **FAR3d Acquisition Results**: Reads the outputs of the FAR3d simulations, plots all eigenfunctions individually, and creates a map image with the whole set of plots arranged as (EP_beta, EP_energy). Returns a data frame (`Output_{Prof}_{n_fam}`) file with selected relevant data from the simulations for further analysis.

<p align="center">
  
![Couplings](/FAR3d_Acquisition_Results/Examples/20.0_0.25.png)
  
</p>

* **Heatmaps**: From the Output of FAR3d simulations, create a heatmap for the Growth rate (left) and Frequency  (right) of Alfvén Eigenmodes as                                      (EP_beta, EP_Energy).
 
<p align="center">
  
![Couplings](/Heatmaps/Heatmaps_(n=3_7_11_15).png)
  
</p>

* **Alfven Continuum Analysis**: Reads the data frame `Output_{Prof}_{n_fam}` and plots in the Alfvén Continuum the excited eigenmodes and their growth rate represented as a color map. The software also creates a new data frame `{Profile}_Maximum_Values` with the excited eigenmodes whose growth rate is the largest for toroidal couplings. 

<p align="center">
  
![Couplings](Data_Analysis/1.%20Experimental%20Profile/Examples/n=5,9,13,17_Contiuum.png "Example for Alfvén Continuumw with AE activity found in FAR3d simulations.")
  
</p>

* **VMEC_reader**: Script reads wout_* VMEC file, prints the variables names, plots the 3D magnetic surface and the poloidal cross-section at the specified toroidal angle of the device. 

<p align="center">
  
![Couplings](/VMEC_reader/TJ-II_new_Magnetic_Surface.gif "")
  
</p>

* **Get_Stellgap**: script that receives the VMEC wout file as input and transforms to Boozer coordinates to obtain the Alfvén Continuum. (In progress).

<p align="center">
  

  
</p>

