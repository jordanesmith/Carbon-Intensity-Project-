from PIL import Image
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_all_non_white_pixels(img, col_names):
    """
    This function takes an image and a list of column names as input and returns a dataframe containing the non-white pixel values of the image.
    
    Parameters:
    img (PIL.Image): The image to process
    col_names (list): The column names for the dataframe
    
    Returns:
    pd.DataFrame: A dataframe containing the non-white pixel values of the image
    """
    
    # convert image to numpy array
    img_arr = np.asarray(img)

    # find non-white pixels and store their values in a list
    non_white_values = np.argwhere(img_arr != 255)
    list_pixel_values_subsection = []
    for i in range(len(non_white_values)):
        vals_ = img_arr[non_white_values[i][0], non_white_values[i][1]]
        list_pixel_values_subsection.append(vals_)

    # create a dataframe from the list of pixel values and column names
    df = pd.DataFrame(list_pixel_values_subsection, columns=col_names)

    return df


def identify_rgb_of_data(df_coloured_pixels, col_names, show_plots=False):
    """
    This function takes a dataframe containing pixel values, a list of column names, and a boolean flag as input. 
    It returns a dictionary containing the mode of each column in the dataframe. If the show_plots flag is set to True,
    it also returns a scatter plot of the data.
    
    Parameters:
    df_coloured_pixels (pd.DataFrame): The dataframe containing the pixel values
    col_names (list): The column names of the dataframe
    show_plots (bool, optional): A flag to indicate whether to show the scatter plots. Default is False.
    
    Returns:
    dict: A dictionary containing the mode of each column in the dataframe
    matplotlib.figure.Figure: A scatter plot of the data, returned only if show_plots is set to True
    """
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
    """
    This function takes an image and a target color dictionary as input, and returns an array of pixel coordinates that match the target color.
    
    Parameters:
    img (PIL.Image): The image to process
    target_col_dict (dict): A dictionary containing the target color values
    
    Returns:
    np.ndarray: An array of pixel coordinates that match the target color
    """

    # convert image to numpy array
    img_arr = np.asarray(img)
    target_arr = np.array([val for val in target_col_dict.values()])
    data_pixels_coords = []
    
    # iterate through each pixel in the image
    for i,row in enumerate(img_arr):
        for j,pixel in enumerate(row):
            if all(pixel == target_arr): # check if pixel values match target color
                if i >= 200: # additional condition to filter pixels
                    data_pixels_coords.append([j,i])

    # convert list of coordinates to numpy array
    arr_data_pix_coords = np.array(data_pixels_coords)
    
    return arr_data_pix_coords

def convolve_image_horizontal_filter(img, width=25):
    """
    This function takes an image and a width as input and returns the result of applying a horizontal convolution filter to the image.
    The filter is a 2D array of [-1, 2, -1] repeated width times.
    
    Parameters:
    img (PIL.Image): The image to process
    width (int, optional): The width of the convolution filter. Default is 25.
    
    Returns:
    np.ndarray: The result of applying the convolution filter to the image
    """

    convolution_kernel = np.array([[-1]*width, 
                                   [2]*width, 
                                   [-1]*width])
    img_arr = np.asarray(img)
    result_x = cv2.filter2D(img_arr, -1, convolution_kernel)
    
    return result_x


def find_data_coordinates(img):
    """
    This function takes an image as input and returns an array of pixel coordinates of the data points in the image.
    It uses a sequence of helper functions to process the image, including finding non-white pixels, identifying the
    target color, and finding the pixel coordinates of the data points.
    
    Parameters:
    img (PIL.Image): The image to process
    
    Returns:
    np.ndarray: An array of pixel coordinates of the data points in the image
    """
    
    col_names = ['r', 'g', 'b']
    df_coloured_pixels = find_all_non_white_pixels(img, col_names)
    target_col_dict = identify_rgb_of_data(df_coloured_pixels, col_names, show_plots=False)
    arr_data_pix_coords = find_all_data_point_pixel_locations(img, target_col_dict)
    
    return arr_data_pix_coords
