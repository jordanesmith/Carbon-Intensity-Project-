# Carbon Intensity Project
## What is it?
This project aims to look at the carbon intensity of the UK electricity grid over a 24 hour cycle, and optimise the charging/ discharging of a residential household battery to minimse CO2.
As part of this project, I have created a function to calculate the carbon intensity from a given battery
charge profile.

## How does it work?
The project uses data from the National Grid ESO's [Carbon Intensity forecast API](https://carbonintensity.org.uk/), with historic predictions and ground truth data.

The carbon intensity API provides data on the carbon intensity of the UK grid, both in the current moment, as well as
for a given time period.

The battery data was provided by a friend who wants to reduce his Carbon Footprint. 

## Where can I find the data?
The data is available in the data folder of the Github repo.

## What Research has been done?
See the Jupyter Notebooks (files ending in `.ipynb`)

## How do I use it?
To use this project, you will need to install the following packages:

- pandas
- numpy
- matplotlib
- seaborn
- pandas-profiling
- sklearn
