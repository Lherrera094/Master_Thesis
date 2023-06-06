<h3 align="center"> Theoretical Study of Alfvénic Stability Optimization for TJ-II Stellerator </h3> 

Supervisor: [Jacobo Varela](https://www.researchgate.net/profile/Jacobo-Varela)

**Description**: The objective is to study the Alfvénic Eigenmodes activity on TJ-II Stellarator with hypotetical operation of NBI heating system for optimization. The analysis is performed using the linear version of the gyro-fluid code FAR3d. The Alfvén Continuum is computed with the STELLGAP code. The AE stability analysis is performed
for the n = 3,7,11, 15, n = 5,9,13, 17, n = 6,10,14 helical families including EP populations with energies in the range of 10 - 90 keV and EP beta from 0.005 to
0.1.


Codes developed to optimize the analysis of the [FAR3d](https://e-archivo.uc3m.es/bitstream/handle/10016/34630/Noninear_NF_2021.pdf?sequence=1) results. The next folder contains

* **Automatization**: Python scripts for faster preparation of launching folder for FAR3d. Scripts developed to launch simulations in cluster URANUS at Universidad Carlos III de Madrid.

* **Rotational Transform Couplings**: General code that obtains the resonant modes for a rotational transform profile. It returns a plot of the resonant modes appearence and the $\iota$ profile, also, an excel with all relevant values. As inputs, it can receives the extremum values, the VMEC wout file or the profile.dat file from FAR3d, the periods for the device (In case of stellarators) and the equilibrium modes. 

<p align="center">
  
![Couplings](/Rotational%20Transform%20Couplings/Examples/delta_iota_0.15_Resonant.png "Example for a 4 period stellarator with high shear.")
  
</p>

* **FAR3d Results Visualization**: Reads the outputs of the FAR3d simulations, plots all eigenfunctions individually and creates a map image with the whole set of plots arranged as (EP_beta,EP_energy). Returns an excel file with important data from the simulations usefull for further analysis called `Output_{Prof}_{n_fam}`.

<p align="center">
  
![Couplings](/FAR3d%20Results%20Visualization/Examples/20.0_0.25.png)
  
</p>

* **Heatmaps**: From the Output of FAR3d simulations, creates a heatmap for Frequency and Growth Rate for the Alfvén Eigenmodes as                                      (EP_beta,EP_Energy).
 
<p align="center">
  
![Couplings](/Heatmaps/Heatmaps_(n=3_7_11_15).png)
  
</p>

* **In Continuum Analysis**: Reads the excel file `Output_{Prof}_{n_fam}` and plot in the Alfvén Continuum at the radial position, the excited eigenmodes and their growth rate represented as a colormap. The software also creates and excel `{Profile}_Maximum_Values` separeted by fast particles profile, with the excited eigenmodes whose growth rate is largest for toroidal couplings. 

<p align="center">
  
![Couplings](/In%20Continuum%20Analysis/Frequency_Experimental%20Profile_Analysis.jpg "Example for Alfvén Continuumw with AE activity found in FAR3d simulations.")
  
</p>

