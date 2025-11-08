# utils/image_analyzer.py

import cv2
import numpy as np
from skimage.restoration import estimate_sigma
from skimage.metrics import structural_similarity as ssim

def analyze_image_repair_type(image_path):
    """
    Analyzes the image from path and returns a list of suggested repair types.
    Example return: ['denoise', 'deblur']
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found or unreadable: {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_float = gray.astype(np.float32) / 255.0

    # 1. Noise Estimation
    sigma_est = estimate_sigma(img_float, channel_axis=None)

    # 2. Blur Estimation via Laplacian
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 3. Compression artifacts (blockiness)
    blockiness = np.mean(np.abs(gray[:, :-1] - gray[:, 1:]))

    # 4. Missing/Corrupted pixels
    missing_pixel_ratio = np.mean((gray < 5) | (gray > 250))

    # 5. Resolution check
    h, w = img.shape[:2]

    suggestions = []
    if sigma_est > 0.08:
        suggestions.append("Denoising (noise detected)")
    if laplacian_var < 50:
        suggestions.append("Deblurring (image appears blurry)")
    if blockiness > 10:
        suggestions.append("Compression artifact removal (blockiness)")
    if missing_pixel_ratio > 0.02:
        suggestions.append("Inpainting (missing/corrupted pixels)")
    if h < 128 or w < 128:
        suggestions.append("Super-resolution (low resolution image)")

    return suggestions
