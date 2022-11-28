import numpy as np
import scipy

from src import image_tools
from src import data_tools
    
def remove_double_peaks(peaks_x, r_arr):
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
    
    # define the HPF parameters
    sos = scipy.signal.butter(1, 1, 'hp', fs=5, output='sos')
    
    def hpf(a):
        return scipy.signal.sosfilt(sos, a)
    
    filtered_arr = np.apply_along_axis(hpf, 0, arr)
    
    return filtered_arr



def find_peaks(arr):
    
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

    img_convolved_horizontal_filter = image_tools.convolve_image_horizontal_filter(img) 
    sum_arr_along_x = np.sum(img_convolved_horizontal_filter, axis=1)
    filtered_sum_arr_along_x = remove_baseline_wander(sum_arr_along_x)
    peaks_x, peaks_y = find_peaks(filtered_sum_arr_along_x)
    y_coord_dict, baseline_y, kw_per_pixel = data_tools.generate_dict_y_coords_for_kW(peaks_x)
    
    return y_coord_dict, baseline_y, kw_per_pixel