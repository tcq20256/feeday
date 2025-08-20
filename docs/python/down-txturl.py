# 批量下载链接文件

import os
import requests

def download_image(url, save_dir):
    # Extract the image filename from the URL
    filename = url.split('/')[-1]
    
    # Create the full path where the image will be saved
    file_path = os.path.join(save_dir, filename)
    
    try:
        # Send a GET request to the image URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Write the image content to a file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved: {file_path}")
        else:
            print(f"Failed to retrieve image from {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def download_images_from_txt(txt_file, save_dir):
    # Check if the directory exists, if not create it
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Read the URLs from the text file
    with open(txt_file, 'r') as file:
        for line in file:
            url = line.strip()
            if url:  # Skip empty lines
                download_image(url, save_dir)

# Specify the path to your text file and the directory to save the images
txt_file = r'g:\Dataset\Image\face\PexelsPortrait\man.txt'  # Replace with the path to your .txt file containing image URLs
save_dir = r'G:\Dataset\Image\face\PexelsPortrait\img'    # Directory where images will be saved

download_images_from_txt(txt_file, save_dir)
