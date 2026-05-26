# CO2 Dynamics in a Mofette: Supplementary Data and Example Programs

## Introduction

This repository contains the supplementary data files and example programs associated with the article titled "CO2 Dynamics in a Mofette: Measurement and Modeling" by Attila Gergely, Alexandru Szakács, Ágnes Gál, and Zoltán Neda. The research investigates the dynamics of CO2 emissions in a mofette located in Covasna, Romania. Using a custom-built remote sensing device, we monitored gas concentrations, temperature, and pressure for seven months. The measurements provided insights into both diurnal cycles and short-term bursts of CO2 emissions, contributing to a better understanding of the gas dynamics within the mofette.

## Contents of the Repository

The repository includes the following:

1. **CO2_raw_data**: Contains the raw data file `CO2_Concentration_Data.txt` with our measurement data.
2. **Example Programs**: Scripts to demonstrate how to use and process the data.
3. **0_README.md**: This file, providing an overview of the data structure and usage instructions.

## Data Description

The raw data is contained in the file `CO2_Concentration_Data.txt`. The data is structured as follows:

- Each measurement is represented by two lines.
- The first line contains the timestamp of the measurement in UTC seconds.
- The second line contains the measured data in a specific format:

### Example Lines from the Data File

1649455396.5622404
b'93512.25 65.00 9.34 93925.87 89.00 8.37 75.60 8.38 74.48 8.48 72.94 8.53 70.99 8.59 69.48 8.74 67.15 8.91 65.19 9.17 62.17 9.46 59.56 9.75 56.56 9.69 52.60 9.47 48.85 9.38 45.32 9.26 40.85 9.28 35.84 9.29 29.83 9.32 23.54 9.26 8.60 9.33 15.15 9.34 4.57 9.46 48.37 8.94 55.18 8.83 61.56 8.77 66.92 8.60  \r\n'
1649455396.5795734
b'93512.25 65.00 9.34 93925.70 89.00 8.37 75.62 8.40 74.51 8.48 72.96 8.55 71.04 8.61 69.43 8.75 66.89 8.90 65.19 9.20 62.06 9.45 59.33 9.73 56.30 9.72 52.24 9.41 48.61 9.40 45.13 9.29 40.63 9.28 35.68 9.27 29.63 9.29 23.34 9.26 8.37 9.34 14.93 9.33 4.52 9.43 48.25 8.92 55.13 8.80 61.44 8.78 66.76 8.58  \r\n'


### Data Structure

1. **Timestamp (First Line)**: The first line in each pair is a floating-point number representing the time of the measurement in UTC seconds.
2. **Measurement Data (Second Line)**: The second line is a string of space-separated values containing the measured data:
   - **First 3 values**: Barometric pressure (measured by the topmost pressure and temperature sensor BMP280), humidity (measured by the topmost humidity sensor DHT11), and temperature (measured by the topmost pressure and temperature sensor BMP280) from the topmost sensor.
   - **Next 3 values**: Barometric pressure, humidity, and temperature (measured by the bottommost sensors BMP280, DHT11).
   - **Next 40 values**: CO2 concentrations and temperatures measured by the STC31 sensors in the main stack from bottom to top. These sensors are placed 5 cm apart in a vertical direction.
   - **Final 8 values**: CO2 concentrations and temperatures measured by the STC31 sensors placed at the side tube illustrated in Figure 2.b from top to bottom. These sensors are placed 10 cm apart in a vertical direction.

### Detailed Data Example

- **Example 1**: `b'93512.25 65.00 9.34 ... 66.92 8.60 \r\n'`
  - `93512.25` - Barometric pressure (topmost BMP280)
  - `65.00` - Humidity (topmost DHT11)
  - `9.34` - Temperature (topmost BMP280)
  - `93925.87` - Barometric pressure (bottommost BMP280)
  - `89.00` - Humidity (bottommost DHT11)
  - `8.37` - Temperature (bottommost BMP280)
  - `75.60 8.38 ... 29.63 9.29` - CO2 concentrations and temperatures from STC31 sensors in the main stack
  - `48.37 8.94 55.18 8.83 61.56 8.77 66.92 8.60` - CO2 concentrations and temperatures from STC31 sensors in the side tube

### Example Code

The example programs provided in this repository demonstrate how to read, filter, and process the data from `CO2_Concentration_Data.txt`. These scripts are designed to help users understand how to work with the data and perform basic analysis.

`1_read_and_plot_raw_CO2_data_example.py`
- **Reading the Data**: The script `read_data` reads the data from the specified file, starting from a given point and reading a specified number of entries. It extracts timestamps, pressure, humidity, temperature, CO2 concentrations, and temperatures from different sensors.
- **Filtering and Conversion**: The script `apply_temperature_conversion` filters out erroneous temperature readings and converts temperature values where necessary (!the conversion is neccessary because of the way how we read the sensors!). It ensures that the data is clean and ready for analysis.
- **Plotting the Data**: The script `plot_data` visualizes the processed data. It plots temperature readings (from the topmost BMP280 sensor, stack, and side tube sensors), pressure readings (from the topmost BMP280 sensor), and CO2 concentration readings (in percentage, from stack and side tube sensors). The plots are labeled with appropriate units and formatted for clarity.

Feel free to explore the example programs and modify them as needed for your analysis.

## Explanation of "2_filter_convert_to_binary_parallel.py"

The script `2_filter_convert_to_binary_parallel.py` is used to clean erroneous sensor readings, fill missing data points via interpolation, and convert the data into a binary format for more efficient processing. This cleaned and processed data was utilized in all analyses presented in the article.

### Functionality

1. **Data Cleaning**: 
    - The script reads raw data from the file `CO2_Concentration_Data.txt`.
    - Erroneous readings are filtered out, and inconsistencies in the time series are corrected.
    - The initial cleanup includes removing the first and last 100 data points and filtering out timestamps that are not in sequential order.

2. **Interpolation**:
    - The script fills in missing data points by interpolation, ensuring continuity in the dataset even when measurements were interrupted.
    - This interpolation is performed using univariate splines, providing smooth transitions between measured points.

3. **Parallel Processing**:
    - To efficiently handle large datasets, the script uses parallel processing.
    - The initial and remaining segments of the data are processed in parallel using multiple CPU cores, speeding up the computation.

4. **Conversion to Binary Format**:
    - After cleaning and interpolation, the data is converted into a binary `.npy` file format.
    - This binary format allows for quicker loading and processing in subsequent analyses.

### Memory Requirements

Due to the large size of the dataset, running this script requires at least 50GB of RAM. To accommodate users who do not have access to such resources, the processed binary data file (`2_CO2_cleaned_data.zip`) is made available for download at the following link: [CO2 Cleaned Data](http://comodi.phys.ubbcluj.ro:8087/supplementary/).

### Usage

Users can run the script to process their own data or use the provided cleaned dataset for analysis. The output file has a `.npy` extension, which can be easily loaded into Python for further examination.

## Example Scripts for Further Analysis

The following example scripts demonstrate how to use the processed binary data file for further analyses. These scripts reproduce several figures from the article:

### `3_Fig_8b_PSD.py`

- **Purpose**: This script calculates and plots the Power Spectral Density (PSD) of CO2 concentration data using Welch's method.
- **Description**: The script loads the processed binary data, extracts CO2 concentration data for a specific sensor, detrends the data, and calculates the PSD. The PSD is then plotted on a log-log scale, and linear fits are performed in specified frequency ranges to analyze different scaling behaviors. The script labels the axes and includes a legend to ensure clarity in the presentation of results.

### `4_Fig8a_time_series.py`

- **Purpose**: This script plots the time series of CO2 concentration for all sensors.
- **Description**: The script loads the processed binary data, extracts timestamps and CO2 concentration data for all sensors, and plots the time series for each sensor. It labels each plot with the appropriate sensor identifier and includes a legend for clarity. This allows for a comprehensive visualization of the CO2 concentration data over time across all sensors.

### `5_Fig4.py`

- **Purpose**: This script plots the time series of CO2 concentration, temperature, and pressure for selected sensors.
- **Description**: The script loads the processed binary data, extracts timestamps, and data for CO2 concentration, temperature, and pressure for specific sensors. It creates subplots for each parameter, ensuring they are synchronized in time. Each subplot is labeled with the appropriate units, and legends are included to differentiate between sensors. This script provides a detailed temporal analysis of the different parameters.

### `6_Fig10_right_panel.py`

- **Purpose**: This script visualizes the temporal variation of CO2 concentration, temperature, and pressure for selected sensors.
- **Description**: The script loads the processed binary data, extracts timestamps and relevant data for CO2 concentration, temperature, and pressure, and creates a series of plots to illustrate their temporal variations. The plots are formatted for clarity, with legends and labels included to ensure the data is easily interpretable. This script highlights the dynamic behavior of the different parameters over time.

These example scripts should provide a comprehensive understanding of how to work with the processed data and reproduce the analyses presented in the article. Feel free to explore and modify these scripts to suit your specific research needs.
