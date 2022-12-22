import numpy as np
import pandas as pd
import os
import datetime



def calculate_pixel_location(y_val_kw, kw_per_pixel, baseline_y):
    
    y_shift = y_val_kw/ kw_per_pixel
    
    return int(baseline_y - y_shift)



def generate_dict_y_coords_for_kW(y_grid_line_coords, y_values_on_graph=[4,2,0,-2,-4]):

    # generate dictionary from these values
    batter_charge_range = max(y_values_on_graph) - min(y_values_on_graph)
    pixel_location_range = max(y_grid_line_coords) - min(y_grid_line_coords)
    kw_per_pixel = -1 * batter_charge_range / pixel_location_range # kW per pixel
    baseline_y = int(np.mean(np.array([max(y_grid_line_coords), min(y_grid_line_coords)]))) # !!!!!! this needs changing if max and min arent +- same number 

    y_coord_dict = {y_val: calculate_pixel_location(y_val, kw_per_pixel, baseline_y) for y_val in y_values_on_graph}
    return y_coord_dict, baseline_y, kw_per_pixel



def generate_csv_all_data(relative_path, file_ending=".csv"):
    
    """ 
    generate a csv with concatenation of all csv data in data/grid/ directory
    
    """
    
    all_csv = [name for name in os.listdir(relative_path) if name.endswith(file_ending)]
    cwd = os.getcwd()

    df_list = []

    for csv_name in all_csv:

        path = os.path.join(cwd, relative_path, csv_name)
        
        try:
            df_list.append(pd.read_csv(path))
        except UnicodeDecodeError: # if files are .xlsx then read_csv doesn't work
            df_list.append(pd.read_excel(path))
            
    all_data = pd.concat(df_list, ignore_index=True).drop_duplicates()
    
    return all_data



def convert_x_data_to_datetime(date_str, data_x_in_seconds):
    
    dtime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    
    new_data = []
    
    for data in data_x_in_seconds:
        converted_data = dtime + datetime.timedelta(seconds=data)
        new_data.append(converted_data)
        
    return np.array(new_data)


def extract_data_for_day(df, date_str):
    
    dtime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day_after = dtime + datetime.timedelta(days=1)
    
    return df.loc[(df['datetime'] > dtime) & (df['datetime'] < day_after)]



def prepare_ci_and_battery_data(day_str, battery_data, ci_data):
    
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




