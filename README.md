# Carbon-Intensity-Project-
## What is it?
This project aims to look at the carbon intensity of the UK electricity grid over a period of time.
As part of this project, I have created a function to calculate the carbon intensity from a given battery
charge profile, and a function to calculate the carbon intensity of a full charge cycle.

## How does it work?
The project uses data from the UK Government's [National Electricity Grid](https://www.nationalgrideso.com/), along
with data from the UK Government's [Carbon Intensity API](https://api.carbonintensity.org.uk/).

The carbon intensity API provides data on the carbon intensity of the UK grid, both in the current moment, as well as
for a given time period.

The National Electricity Grid provides data on the power supplied to the UK grid, broken down by source.

## Where can I find the data?
The data is available in the data folder of the Github repo.

## How do I use it?
To use this project, you will need to install the following packages:

- pandas
- numpy
- matplotlib
- seaborn
- pandas-profiling
- sklearn