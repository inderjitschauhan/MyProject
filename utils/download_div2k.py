import os
import requests
from zipfile import ZipFile

# Define your target folder
save_dir = r"C:\Users\inder\Documents\Final Project\Code\data\Dataset\DIV2K"
os.makedirs(save_dir, exist_ok=True)

# URLs for DIV2K LR and HR images (x2)
urls = {
    "train_LR": "https://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X2.zip",
    "valid_LR": "https://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X2.zip",
    "train_HR": "https://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_HR.zip",
    "valid_HR": "https://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_HR.zip",
}

def download_and_extract(name, url, save_path):
    zip_path = os.path.join(save_path, f"{name}.zip")
    if not os.path.exists(zip_path):
        print(f"Downloading {name}...")
        response = requests.get(url, stream=True)
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"{name}.zip already exists, skipping download.")

    # Extract
    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(os.path.join(save_path, name))
    print(f"{name} extracted successfully.")

for name, url in urls.items():
    download_and_extract(name, url, save_dir)
