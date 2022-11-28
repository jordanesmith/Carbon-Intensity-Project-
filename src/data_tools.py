import numpy as np



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