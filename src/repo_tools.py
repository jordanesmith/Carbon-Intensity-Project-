import os

def shorten_image_file_names(old_img_paths, cwd):
    """
    This function takes a dictionary of old image file paths and the current working directory as input, 
    and shortens the names of the images by replacing them with the last 10 characters of the original name.
    It also moves the images to a "data/images" directory within the current working directory.
    
    Parameters:
    old_img_paths (dict): A dictionary of old image file paths
    cwd (str): The current working directory 
    
    Returns:
    None
    """

    for img in old_img_paths:
        if "Screenshot" in img:
            new_name = img[-10:]
            new_path = os.path.join(cwd, "data", "images", new_name)
            old_path = old_img_paths[img]
            os.rename(old_path, new_path)
            
    path_to_imgs = os.path.join(cwd, "data", "images")
    
    print(f"files renamed, check {path_to_imgs}")
