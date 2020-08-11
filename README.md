# MLTravelTimesFigures
Code to reproduce figures for paper Estimating the travel time and most likely path from Lagrangian drifters.


## Setup:
Instructions below will get you to the point where you can run the .ipynb files.


Install package at https://github.com/MikeOMa/DriftMLP.

I advise doing this in a new environment using conda. To create environment run 
```
conda create --name mlpath python=3.7
conda activate mlpath
```
then install package by running instructions on the github link above. Also complete the first stage of setup by downloading the drifter dataset.
 add kernel to jupyter spec 
```
 conda install ipykernel`
 python -m ipykernel install --user --name mlpath`
```
Finally start a jupyter notebook and navigate to where you have downloaded this directory to.

In any file below which has `os.environ['DRIFTFILE']` you will need to replace this with a path to where the .h5 file containing the drifter data was created when setting up DriftMLP. 
Alternatively, set an environment variable 'DRIFTFILE' which holds the name to where the .h5 file can be found.

## Order of running

`MakeRotations.py` currently this script is set to use 10 rotations to make it run quickly. The paper figures were produced by setting this to 100 rotations.

`MakeDefNetworks.py` Makes the default non-rotated networks. The discretized drifter trajectories are also saved within these networks for bootstrap

`bootstrap_network.py` loads in the output of `MakeDefNetworks.py` then saves 200 bootstrapped networks.

 `FiguresForPaper.ipynb` requires all the above to be run. If not using 100 rotations or 200 bootstrap samples the file names must be changed where the files are read in.
 
 `SupplementaryInformation.ipynb` requires both `MakeDefNetworks.py` and `MakeRotations.py` to be run. This script conducts the sensitivity analysis.
 
 Finally, `locationsplot.py` is a standalone script which makes the currents plot. In addition to the packages required for the paper, xarray will be needed. Install via `pip install xarray`. The data will also be required, we use the Annual mean values version here [link to global drifter program website for data](https://www.aoml.noaa.gov/phod/gdp/mean_velocity.php)

