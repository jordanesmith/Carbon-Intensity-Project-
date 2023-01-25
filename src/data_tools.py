import numpy as np
import pandas as pd
import os
import datetime


def calculate_pixel_location(y_val_kw, kw_per_pixel, baseline_y):
    """
    Calculates the pixel location of a y-value in kW on a graph.
    
    Args:
    y_val_kw (float): The y-value in kW.
    kw_per_pixel (float): The ratio of kW per pixel on the graph.
    baseline_y (int): The baseline y-coordinate of the graph.
    
    Returns:
    int: The pixel location of the y-value on the graph.
    """
    y_shift = y_val_kw/ kw_per_pixel
    return int(baseline_y - y_shift)


def generate_dict_y_coords_for_kW(y_grid_line_coords, y_values_on_graph=[4,2,0,-2,-4]):
    """
    Generates a dictionary of y-coordinates for y-values in kW on a graph.
    
    Args:
    y_grid_line_coords (list): A list of y-coordinates for the grid lines on the graph.
    y_values_on_graph (list): A list of y-values in kW that should be included in the dictionary.
    
    Returns:
    tuple: A tuple containing the y-coordinate dictionary, the baseline y-coordinate, and the ratio of kW per pixel.
    """
    batter_charge_range = max(y_values_on_graph) - min(y_values_on_graph)
    pixel_location_range = max(y_grid_line_coords) - min(y_grid_line_coords)
    kw_per_pixel = -1 * batter_charge_range / pixel_location_range 
    baseline_y = int(np.mean(np.array([max(y_grid_line_coords), min(y_grid_line_coords)])))
    y_coord_dict = {y_val: calculate_pixel_location(y_val, kw_per_pixel, baseline_y) for y_val in y_values_on_graph}
    return y_coord_dict, baseline_y, kw_per_pixel


def generate_csv_all_data(relative_path, file_ending=".csv"):
    """
    Generates a DataFrame with the concatenation of all data in a specified directory. The function will try to read the files as csv and if it can't it will try to read them as xlsx
    
    Args:
    relative_path (str): The relative path of the directory containing the data files.
    file_ending (str): The file ending of the data files. Default is ".csv"
    
    Returns:
    pd.DataFrame: A DataFrame with all the data from the concatenated files.
    """
    all_data_files = [name for name in os.listdir(relative_path) if name.endswith(file_ending)]
    cwd = os.getcwd()
    df_list = []
    for data_file in all_data_files:
        path = os.path.join(cwd, relative_path, data_file)
        try:
            df_list.append(pd.read_csv(path))
        except UnicodeDecodeError: # if files are not in .csv format, try reading them as .xlsx
            df_list.append(pd.read_excel(path))
    all_data = pd.concat(df_list, ignore_index=True).drop_duplicates()
    return all_data


def convert_x_data_to_datetime(date_str, data_x_in_seconds):
    """
    Convert data on x-axis to datetime format
    
    Parameters:
    date_str (str) : date in string format (YYYY-MM-DD)
    data_x_in_seconds (ndarray) : array of x-axis data in seconds
    
    Returns:
    ndarray : array of x-axis data in datetime format
    """
    dtime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    new_data = []
    
    for data in data_x_in_seconds:
        converted_data = dtime + datetime.timedelta(seconds=data)
        new_data.append(converted_data)
        
    return np.array(new_data)


def extract_data_for_day(df, date_str):
    """
    Filter dataframe to extract data for a specific day
    
    Parameters:
    df (dataframe) : dataframe containing datetime column
    date_str (str) : date in string format (YYYY-MM-DD)
    
    Returns:
    dataframe : filtered dataframe
    """
    dtime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day_after = dtime + datetime.timedelta(days=1)
    
    return df.loc[(df['datetime'] > dtime) & (df['datetime'] < day_after)]



def prepare_ci_and_battery_data(day_str, battery_data, ci_data):
    """
    Prepare Carbon Intensity (CI) and battery data for a specific day
    
    Parameters
    ----------
    day_str : str
        date string in format 'YYYY-MM-DD'
    battery_data : DataFrame
        dataframe containing battery data
    ci_data : DataFrame
        dataframe containing carbon intensity data
        
    Returns
    -------
    ci_and_battery_data : DataFrame
        dataframe containing the concatenated data of the filtered CI and battery data for the specific day
    """
    
    # filter data from specific day
    battery_data_for_day = extract_data_for_day(battery_data, day_str)
    ci_data_for_day = extract_data_for_day(ci_data, day_str)

    # interpolate ci_data to align with battery_data
    time_intervals = battery_data_for_day["datetime"]
    ci_data_y = ci_data_for_day["Actual Carbon Intensity (gCO2/kWh)"]
    new_x_coords = np.arange(len(time_intervals)) * len(ci_data_y) / len(time_intervals)
    interpolated_ci_data = np.interp(new_x_coords, np.arange(len(ci_data_y)), ci_data_y.astype("float"))

    # format the array
    times = pd.Series(battery_data_for_day["datetime"].to_numpy(), name="datetime")
    battery_vals = pd.Series(battery_data_for_day["NetChargingRate(kW)"].to_numpy(), name="battery_power_consumption/kW") 
    ci_vals = pd.Series(interpolated_ci_data, name='act_carbon_intensity/(gCO2/kWh)')

    ci_and_battery_data = pd.concat([times,ci_vals,battery_vals],axis=1)
    
    return ci_and_battery_data

