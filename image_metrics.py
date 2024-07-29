import os
import cv2
import numpy as np
import pandas as pd
import sys
from tqdm import tqdm
from image_similarity_measures.quality_metrics import ssim, fsim, psnr

def pad_to_square(image):
    """Pad image to make it square by adding black padding to the shorter side."""
    h, w = image.shape[:2]
    if h == w:
        return image
    size = max(h, w)
    padded_image = np.zeros((size, size, 3), dtype=np.uint8) if len(image.shape) == 3 else np.zeros((size, size), dtype=np.uint8)
    pad_vert = (size - h) // 2
    pad_horz = (size - w) // 2
    padded_image[pad_vert:pad_vert + h, pad_horz:pad_horz + w] = image
    return padded_image

def preprocess_image(image, save_path, filename, size=(256, 256)):
    """Preprocess image by padding it to square, resizing to given size, and saving it."""
    padded_image = pad_to_square(image)
    resized_image = cv2.resize(padded_image, size, interpolation=cv2.INTER_AREA)
    # Save the padded image
    #cv2.imwrite(os.path.join(save_path, filename), resized_image)
    return resized_image

def calculate_metrics(ct_image, hist_image):
    """Calculate SSIM, FSIM, and PSNR between two images."""
    ssim_value = ssim(ct_image, hist_image)
    fsim_value = fsim(ct_image, hist_image)
    psnr_value = psnr(ct_image, hist_image)
    return ssim_value, fsim_value, psnr_value

def main(ct_file):
    ct_folder = '../data/all_data/CT'
    hist_folder = '../data/all_data/Hist'
    csv_file = 'metrics.csv'
    padded_folder = 'Padded'

    print(f"Current working directory: {os.getcwd()}")

    if not os.path.exists(ct_folder):
        print(f"CT folder '{ct_folder}' does not exist.")
        return

    if not os.path.exists(hist_folder):
        print(f"Hist folder '{hist_folder}' does not exist.")
        return

    if not os.path.exists(padded_folder):
        os.makedirs(padded_folder)

    ct_file_path = os.path.join(ct_folder, ct_file)

    if not os.path.exists(ct_file_path):
        print(f"CT image file {ct_file_path} does not exist.")
        print("Available files in the CT folder:")
        print(os.listdir(ct_folder))
        return

    ct_image = cv2.imread(ct_file_path, cv2.IMREAD_GRAYSCALE)
    ct_image = cv2.cvtColor(ct_image, cv2.COLOR_GRAY2RGB)
    ct_image = preprocess_image(ct_image, padded_folder, ct_file)

    hist_files = [f for f in os.listdir(hist_folder) if os.path.isfile(os.path.join(hist_folder, f))]

    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=['CT Image', 'Histology Image', 'SSIM', 'FSIM', 'PSNR'])
    else:
        df = pd.DataFrame(columns=['CT Image', 'Histology Image', 'SSIM', 'FSIM', 'PSNR'])

    results = []

    # Progress bar for histology images
    for hist_file in tqdm(hist_files, desc="Processing histology images", leave=False):
        try:
            hist_path = os.path.join(hist_folder, hist_file)
            hist_image = cv2.imread(hist_path)
            hist_image = preprocess_image(hist_image, padded_folder, hist_file)

            ssim_value, fsim_value, psnr_value = calculate_metrics(ct_image, hist_image)

            # Check if the pair already exists in the DataFrame
            mask = (df['CT Image'] == os.path.basename(ct_file)) & (df['Histology Image'] == hist_file)
            if mask.any():
                # Update existing entry
                df.loc[mask, ['SSIM', 'FSIM', 'PSNR']] = ssim_value, fsim_value, psnr_value
            else:
                # Add new entry
                results.append({
                    'CT Image': os.path.basename(ct_file),
                    'Histology Image': hist_file,
                    'SSIM': ssim_value,
                    'FSIM': fsim_value,
                    'PSNR': psnr_value
                })

        except Exception as e:
            print(f"Error processing {hist_file} with {ct_file}: {e}")

    # Append new results to the DataFrame if results is not empty
    if results:
        df = pd.concat([df, pd.DataFrame(results)], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)
    print(f"Metrics for {ct_file} saved to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_metrics.py <ct_image_file>")
    else:
        ct_file = sys.argv[1]
        main(ct_file)
