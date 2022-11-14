import os

def shorten_image_file_names(old_img_paths, cwd):

    for img in old_img_paths:
        if "Screenshot" in img:
            new_name = img[-10:]
            new_path = os.path.join(cwd, "data", "images", new_name)
            old_path = old_img_paths[img]
            os.rename(old_path, new_path)
            
    path_to_imgs = os.path.join(cwd, "data", "images")
    
    print(f"files renamed, check {path_to_imgs}")