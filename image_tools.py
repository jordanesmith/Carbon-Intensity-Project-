from PIL import Image
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



