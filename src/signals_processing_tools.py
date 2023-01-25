import numpy as np
import scipy

from src import image_tools
from src import data_tools
    
def remove_double_peaks(peaks_x, r_arr):
    """
    This function takes the x-coordinates of peaks and the values of a signal as input, and returns a list of peaks
    where only one peak is kept in case of a double peak.
    
    Parameters:
    peaks_x (np.ndarray): The x-coordinates of the peaks
    r_arr (np.ndarray): The values of the signal
    
    Returns:
    list: The x-coordinates of the peaks with double peaks removed
    """
    peaks_y = r_arr[peaks_x]
    chosen_peaks = []
    for i,peak in enumerate(peaks_x):
        if i != len(peaks_x)-1:
            if abs(peaks_x[i+1] - peak) / peaks_x[-1] < 0.05:
                if peaks_y[i] <= peaks_y[i+1]:
                    chosen_peaks.append(peak)
                else:
                    chosen_peaks.append(peaks_x[i+1])
            elif abs(peaks_x[i-1] - peak) / peaks_x[-1] < 0.05:
                pass
            
            else:
                chosen_peaks.append(peak) # this is for the case where single peak detected amongst double peaks     
            
    return chosen_peaks

def remove_baseline_wander(arr):
    """
    This function takes an array as input and returns the array with the baseline wander removed.
    It uses a high-pass filter with a cutoff frequency of 1 and a sample rate of 5.
    
    Parameters:
    arr (np.ndarray): The array to process

    Returns:
    np.ndarray: The array with the baseline wander removed
    """

    # define the HPF parameters
    sos = scipy.signal.butter(1, 1, 'hp', fs=5, output='sos')

    def hpf(a):
        return scipy.signal.sosfilt(sos, a)

    filtered_arr = np.apply_along_axis(hpf, 0, arr)

    return filtered_arr


def find_peaks(arr):
    """
    This function takes an array as input, removes the baseline wander, detects the peaks and removes double peaks.
    It returns the x-coordinates and y-coordinates of the peaks.

    Parameters:
    arr (np.ndarray): The array to process

    Returns:
    tuple: A tuple containing the x-coordinates and y-coordinates of the peaks
    """

    # filter array to remove baseline wander 
    filtered_sum_arr_along_x = remove_baseline_wander(arr)

    # detect peaks
    r_arr = arr[:,0] # only run calculations on r component of pixel values
    peaks_x = scipy.signal.find_peaks(r_arr, height=0.7*max(r_arr))[0]
    peaks_x = [peak for peak in peaks_x if peak >= 200] # remove the peaks not wanted on the left 

    peaks_x = remove_double_peaks(peaks_x, r_arr)
    peaks_y = r_arr[peaks_x]
    
    return peaks_x, peaks_y


def compute_y_calibrations(img):
    """
    This function takes an image as input, convolves it with a horizontal filter, and finds the y-coordinates of the peaks.
    It then generates a dictionary of y-coordinates, the baseline y-coordinate and the kW per pixel.
    
    Parameters:
    img (PIL.Image.Image): The image to process
    
    Returns:
    tuple: A tuple containing the y-coordinate dictionary, the baseline y-coordinate and the kW per pixel
    """

    # convolve image with horizontal filter
    img_convolved_horizontal_filter = image_tools.convolve_image_horizontal_filter(img) 

    # sum the image along the x-axis
    sum_arr_along_x = np.sum(img_convolved_horizontal_filter, axis=1)

    # remove baseline wander
    filtered_sum_arr_along_x = remove_baseline_wander(sum_arr_along_x)

    # find peaks
    peaks_x, peaks_y = find_peaks(filtered_sum_arr_along_x)

    # generate y-coordinate dictionary, baseline y-coordinate and kW per pixel
    y_coord_dict, baseline_y, kw_per_pixel = data_tools.generate_dict_y_coords_for_kW(peaks_x)

    return y_coord_dict, baseline_y, kw_per_pixel


