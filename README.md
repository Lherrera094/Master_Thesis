# Master_Thesis
Series of codes created to optimize the analysis of the FAR3d outputs.

Automatization Folder: Contains the scripts to create the folders with the Input characteristics the user wish to study and launch FAR3d simulations in a                          much faster way. It was develop to use it in the cluster URANUS in Universidad Carlos III de Madrid.

Rotational Transform Couplings: It gives the toroidal couplings with the relevant poloidal couplings, and iota profile. The outputs for couplings are                                       represented in two graphs and an excel with all relevant values. As inputs, it receives the profile.dat file from FAR3d and                                 the periods for the device.

FAR3d Results Visualization: Reads the outputs of the FAR3d simulations, plots all eigenfunctions individualy and creates an image with the whole set of                                plots in arranged as (EP_beta,EP_energy). Returns an excel file with important data from the simulations usefull for analysis                              called "Output_{Prof}_{n_fam}".

In Continuum Analysis: Reads the excel file "Output_{Prof}_{n_fam}" and plot in the Alfvén Continuum at the radial position, the excited eigenmodes and                            their growth rate represented as a colormap. The software . Also creates and excel "{Profile}_Maximum_Values" separeted by NBI                              profile, with the excited eigenmodes whose growth rate is largest for toroidal couplings. 

Frequency and GrowthRate Heatmaps: From the Output of the FAR3d simulations, creates a series of heatmaps of Frequency and Growth Rate with configuration                                      (EP_beta,EP_Energy).

