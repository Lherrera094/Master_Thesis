<h3 align="center"> Theoretical Study of Alfvénic Stability Optimization for TJ-II Stellerator </h3> 

Supervisor: [Jacobo Varela](https://www.researchgate.net/profile/Jacobo-Varela)

Series of codes created to optimize the analysis of the [FAR3d](https://e-archivo.uc3m.es/bitstream/handle/10016/34630/Noninear_NF_2021.pdf?sequence=1) outputs.

* **Automatization**: Contains the scripts to create the folders with the Input characteristics the user wish to study and launch FAR3d simulations in a much faster way. It was develop to be use in the cluster URANUS at Universidad Carlos III de Madrid.

* **Rotational Transform Couplings**: It gives the toroidal couplings with their respective poloidal couplings, and rotational transform profile. The outputs for couplings are represented in two graphs and an excel with all relevant values. As inputs, it receives the profile.dat file from FAR3d and the periods for the device.

<p align="center">
  
![Couplings](/Rotational%20Transform%20Couplings/Examples/1.5_iota_Couplings.png "Example for a 4 period stellarator with high shear.")
  
</p>

* **FAR3d Results Visualization**: Reads the outputs of the FAR3d simulations, plots all eigenfunctions individually and creates a map image with the whole set of plots arranged as (EP_beta,EP_energy). Returns an excel file with important data from the simulations usefull for further analysis called `Output_{Prof}_{n_fam}`.

<p align="center">
  
![Couplings](/FAR3d%20Results%20Visualization/Examples/20.0_0.1.png)
  
</p>

* **In Continuum Analysis**: Reads the excel file `Output_{Prof}_{n_fam}` and plot in the Alfvén Continuum at the radial position, the excited eigenmodes and their growth rate represented as a colormap. The software also creates and excel `{Profile}_Maximum_Values` separeted by fast particles profile, with the excited eigenmodes whose growth rate is largest for toroidal couplings. 

<p align="center">
  
![Couplings](/In%20Continuum%20Analysis/Frequency_Experimental%20Profile_Analysis.jpg "Example for Alfvén Continuumw with AE activity found in FAR3d simulations.")
  
</p>

* **Heatmaps**: From the Output of FAR3d simulations, creates a series of heatmaps of Frequency and Growth Rate with configuration                                      (EP_beta,EP_Energy) to show the change of Alfvén Eigenmodes.
* 
<p align="center">
  
![Couplings](/Heatmaps/Heatmaps_(n=3_7_11_15)_git.png)
  
</p>
