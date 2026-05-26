CO2 Dynamics in a Mofette: Supplementary Data and Example Programs
Introduction

This repository contains the supplementary data files and example programs associated with the article titled "CO2 Dynamics in a Mofette: Measurement and Modeling" by Attila Gergely, Alexandru Szakács, Ágnes Gál, and Zoltán Neda. The research investigates the dynamics of CO2 emissions in a mofette located in Covasna, Romania. Using a custom-built remote sensing device, we monitored gas concentrations, temperature, and pressure for seven months. The measurements provided insights into both diurnal cycles and short-term bursts of CO2 emissions, contributing to a better understanding of the gas dynamics within the mofette.
Contents of the Repository

The repository includes the following:

    CO2_raw_data: Contains the raw data file CO2_Concentration_Data.txt with our measurement data.
    Example Programs: Scripts to demonstrate how to use and process the data.
    0_README.md: This file, providing an overview of the data structure and usage instructions.

Data Description

The raw data is contained in the file CO2_Concentration_Data.txt. The data is structured as follows:

    Each measurement is represented by two lines.
    The first line contains the timestamp of the measurement in UTC seconds.
    The second line contains the measured data in a specific format:

Example Lines from the Data File

1649455396.5622404 b'93512.25 65.00 9.34 93925.87 89.00 8.37 75.60 8.38 74.48 8.48 72.94 8.53 70.99 8.59 69.48 8.74 67.15 8.91 65.19 9.17 62.17 9.46 59.56 9.75 56.56 9.69 52.60 9.47 48.85 9.38 45.32 9.26 40.85 9.28 35.84 9.29 29.83 9.32 23.54 9.26 8.60 9.33 15.15 9.34 4.57 9.46 48.37 8.94 55.18 8.83 61.56 8.77 66.92 8.60 \r\n' 1649455396.5795734 b'93512.25 65.00 9.34 93925.70 89.00 8.37 75.62 8.40 74.51 8.48 72.96 8.55 71.04 8.61 69.43 8.75 66.89 8.90 65.19 9.20 62.06 9.45 59.33 9.73 56.30 9.72 52.24 9.41 48.61 9.40 45.13 9.29 40.63 9.28 35.68 9.27 29.63 9.29 23.34 9.26 8.37 9.34 14.93 9.33 4.52 9.43 48.25 8.92 55.13 8.80 61.44 8.78 66.76 8.58 \r\n'
Data Structure

    Timestamp (First Line): The first line in each pair is a floating-point number representing the time of the measurement in UTC seconds.
    Measurement Data (Second Line): The second line is a string of space-separated values containing the measured data:
        First 3 values: Barometric pressure (measured by the topmost pressure and temperature sensor BMP280), humidity (measured by the topmost humidity sensor DHT11), and temperature (measured by the topmost pressure and temperature sensor BMP280) from the topmost sensor.
        Next 3 values: Barometric pressure, humidity, and temperature (measured by the bottommost sensors BMP280, DHT11).
        Next 40 values: CO2 concentrations and temperatures measured by the STC31 sensors in the main stack from bottom to top. These sensors are placed 5 cm apart in a vertical direction.
        Final 8 values: CO2 concentrations and temperatures measured by the STC31 sensors placed at the side tube illustrated in Figure 2.b from top to bottom. These sensors are placed 10 cm apart in a vertical direction.

Detailed Data Example

    Example 1: b'93512.25 65.00 9.34 ... 66.92 8.60 \r\n'
        93512.25 - Barometric pressure (topmost BMP280)
        65.00 - Humidity (topmost DHT11)
        9.34 - Temperature (topmost BMP280)
        93925.87 - Barometric pressure (bottommost BMP280)
        89.00 - Humidity (bottommost DHT11)
        8.37 - Temperature (bottommost BMP280)
        75.60 8.38 ... 29.63 9.29 - CO2 concentrations and temperatures from STC31 sensors in the main stack
        48.37 8.94 55.18 8.83 61.56 8.77 66.92 8.60 - CO2 concentrations and temperatures from STC31 sensors in the side tube

Memory Requirements

The pre-processed binary data file (2_CO2_cleaned_data.zip) is made available for download at the following link: CO2 Cleaned Data.

Or data at:https://drive.google.com/file/d/19KDUMp-DDpKJkSfg13eaJfdgW5kH0cEd/view?usp=drive_link (cleaned) and https://drive.google.com/file/d/1V1z_enBFFWFfgotWdfKWJOkKXShhGfVx/view?usp=drive_link (raw)