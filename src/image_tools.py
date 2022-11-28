from PIL import Image

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def find_all_non_white_pixels(img, col_names):

    img_arr = np.asarray(img)

    # generate dataframe and array of non-white pixel values 
    non_white_values = np.argwhere(img_arr != 255)
    list_pixel_values_subsection = []
    for i in range(len(non_white_values)):
        vals_ = img_arr[non_white_values[i][0], non_white_values[i][1]]
        list_pixel_values_subsection.append(vals_)

    df = pd.DataFrame(list_pixel_values_subsection, columns=col_names)

    return df


def identify_rgb_of_data(df_coloured_pixels, col_names, show_plots=False):

    if show_plots:
        fig, axs = plt.subplots(3)
    
    target_col_dict = {}
    
    for i,col in enumerate(col_names):
        y = df_coloured_pixels[col]
        target_col_dict[col] = y.mode().values[0]
        
        if show_plots:
            axs[i].scatter(np.arange(len(y)), y, label=col, c=np.array(df_coloured_pixels[col_names])/255)
            axs[i].set_title(f"{col} with mode: {y.mode().values[0]}")
            axs[i].set_ylim(0,255)
        
    if show_plots:
        return target_col_dict, fig.tight_layout()
    else:
        return target_col_dict
    

def find_all_data_point_pixel_locations(img, target_col_dict):

    img_arr = np.asarray(img)
    target_arr = np.array([val for val in target_col_dict.values()])
    data_pixels_coords = []
    for i,row in enumerate(img_arr):
        for j,pixel in enumerate(row):
            if all(pixel == target_arr): # without this, the pixels top left from the colour label in original image will be detected
                if i >= 200:
                    data_pixels_coords.append([j,i])

    arr_data_pix_coords = np.array(data_pixels_coords)
    
    return arr_data_pix_coords



def convolve_image_horizontal_filter(img, width=25):

    convolution_kernel = np.array([[-1]*width, 
                                   [2]*width, 
                                   [-1]*width])
    img_arr = np.asarray(img)
    result_x = cv2.filter2D(img_arr, -1, convolution_kernel)
    
    return result_x



def find_data_coordinates(img):
    # Bring it all together
    
    col_names = ['r', 'g', 'b']
    df_coloured_pixels = find_all_non_white_pixels(img, col_names)
    target_col_dict = identify_rgb_of_data(df_coloured_pixels, col_names, show_plots=False)
    arr_data_pix_coords = find_all_data_point_pixel_locations(img, target_col_dict)
    
    return arr_data_pix_coords



