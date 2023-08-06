## A brief overview of the package objective
The main objective of the nembem package is to calculate the tangential and normal loads experienced by the DTU 10 MW turbine blades. The load calculations are based on a blade element momentum theory (BEM) algorithm which calculates local loads based on a user specified incoming wind speed. The nembem package includes a function called bem, that either assumes steady flow (non-turbulent) or unsteady flow (turbulent). 
Furthermore, functions that can visualize turbine overview, airfoil data and blade loadings are include in the package

Til docstring: 
When using the blade element momentum theory (BEM) algorithm, the simulation has a transient time where the code converge towards the correct result. One should therefore ignore results from the transient time. When using steady BEM, as in the nembem does, the transient time is generally equal to 3-5 timesteps. Unless other is specified as keyword, one timestep is 0.1 second.

The DTU 10 MW  cut in windspeed is 4 m/s and the cut out windspeed is 25 m/s, so if the windspeed is not 4 m/s < windspeed < 25 m/s then the turbine loads will be 0.

The rated windspeed of the DTU 10 MW is 11.4 m/s and the rated power is 10.64 MW. Therefore, if 11.4 m/s < windspeed < 25 m/s, then the power output will be 10.64 MW. 

## Installation instructions
Installation for Python by using Anaconda Terminal: 
Have a network connection and write following 

- pip install nembem

This installs the packages on your computer. To use the package, write following in start of your script: import nembem

## Requirements
The package use the packages numpy and matplotlip. These should therefore be installed.

## Tutorials
For tutorials of how to use the different functions included in the package, see the folder called "tutorials". 

## Package structure

nembem/  
├── __init__.py  
├── tutorials  
│   ├── bem_tutorial  
│   └── visualization_tutorial  
├── dtu_10_mw_class.py  
│   ├── get_area  
│   ├── visualize_turbine  
│   ├── plot_airfoil_data  
│   └── bem  
├── functions.py  
│   ├── tm_yaw_tilt_roll  
│   ├── rotate_blades  
│   ├── load_force_coeff_files  
│   ├── interp_force_coeffs  
│   ├── write_mann_input  
│   └── load_turb_box  
├── input/  
│   ├──  bladedat.txt  
│   ├──  cylinder.txt  
│   ├──  FFA-W3-241.txt  
│   ├──  FFA-W3-301.txt  
│   ├──  FFA-W3-360.txt  
│   ├──  FFA-W3-480.txt  
│   ├──  FFA-W3-600.txt  
│   └──  sky.JPG  
├── sim1.bin  
├── sim2.bin  
└── sim3.bin  
## Peer review 
We did not get peer review feedback on this package.

## Git workflow
Adam and Toke has coded most of the project while together so the need for branching and merging has been limited. Programming and co-programming has been done by turns.

## Contact Info

Adam Vejstrup: s193870@student.dtu.dk  
Toke Schäffer: s193878@student.dtu.dk

## License
This project is licensed under the MIT License
