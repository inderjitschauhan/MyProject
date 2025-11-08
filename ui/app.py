# =====================================================================
# STREAMLIT IMAGE RESTORATION APP
# =====================================================================
# This script allows users to upload an image, detect its repair type,
# and apply various denoising algorithms. It includes debug setup for
# proper module imports and handles multiple repair methods.
# =====================================================================

# ---------- DEBUG PATH SETUP (for troubleshooting imports) ----------
import sys, os
from pathlib import Path
import traceback

def _debug_path_setup():
    print("----- DEBUG: streamlit import troubleshooting -----")
    cwd = Path.cwd()
    print(f"CURRENT WORKING DIRECTORY: {cwd}")
    this_file = Path(__file__).resolve()
    print(f"__file__ resolved to: {this_file}")
    print(f"Parents: {this_file.parents[:]}") 
    print("sys.path (start):")
    for i, p in enumerate(sys.path[:10]):
        print(f"  {i}: {p}")

    # Assume folder structure:
    # <PROJECT_ROOT>/ui/app.py
    # <PROJECT_ROOT>/utils/...
    project_root = this_file.parents[1]
    print(f"Assuming project root is: {project_root}")

    # Ensure project root is in sys.path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Inserted project root into sys.path: {project_root}")
    else:
        print("Project root already on sys.path")

    print("sys.path (after insert):")
    for i, p in enumerate(sys.path[:10]):
        print(f"  {i}: {p}")

    # Verify utils module
    candidate = project_root / "utils" / "image_analyzer.py"
    print(f"Checking for expected file: {candidate} -> exists: {candidate.exists()}")
    if candidate.exists():
        print("File is present. Attempting import test...")
        try:
            import importlib
            mod = importlib.import_module("utils.image_analyzer")
            print("SUCCESS: imported utils.image_analyzer")
            if hasattr(mod, "analyze_image_repair_type"):
                print("SUCCESS: found analyze_image_repair_type function")
            else:
                print("WARNING: analyze_image_repair_type NOT found")
        except Exception:
            print("IMPORT FAILED — full traceback:")
            traceback.print_exc()
    else:
        print("ERROR: expected file utils/image_analyzer.py not found.")
    print("----- END DEBUG -----\n")

# Run path setup check
_debug_path_setup()

# =====================================================================
# IMPORTS
# =====================================================================
import streamlit as st
from PIL import Image
import time
import numpy as np
from utils.image_analyzer import analyze_image_repair_type

# Image quality metrics
from skimage.metrics import peak_signal_noise_ratio as sk_psnr
from skimage.metrics import structural_similarity as sk_ssim
import torch


# =====================================================================
# FUNCTION: LPIPS COMPUTATION
# =====================================================================
def compute_lpips(img1, img2, net="alex"):
    """
    Compute the Learned Perceptual Image Patch Similarity (LPIPS)
    metric between two images.
    """
    import lpips
    device = "cuda" if torch.cuda.is_available() else "cpu"
    loss_fn = lpips.LPIPS(net=net).to(device)

    def to_tensor(pil_img):
        arr = np.array(pil_img.convert("RGB")).astype(np.float32) / 255.0
        t = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0)
        t = (t - 0.5) * 2.0
        return t.to(device)

    with torch.no_grad():
        d = loss_fn(to_tensor(img1), to_tensor(img2))
    return float(d.squeeze().cpu().numpy())


# =====================================================================
# STREAMLIT APP CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Image Restoration", layout="wide")
st.title("Image Restoration")
st.write("Upload an image to analyze and denoise using smart agents.")


# =====================================================================
# FILE UPLOAD SECTION
# =====================================================================
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Open and preprocess image
        image = Image.open(uploaded_file)
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # Save input image
        input_dir = "data/distort_images"
        os.makedirs(input_dir, exist_ok=True)
        input_path = os.path.join(input_dir, "sample_image.png")
        image.save(input_path)

        # Clean and prepare output directory
        repaired_dir = "data/repaired_images"
        os.makedirs(repaired_dir, exist_ok=True)
        for file in os.listdir(repaired_dir):
            os.remove(os.path.join(repaired_dir, file))

        st.write(f"Image saved to: {input_path}")
        st.subheader("Preview of Uploaded Image")
        st.image(image, caption="Distorted Uploaded Image", use_container_width=False)

        # =================================================================
        # IMAGE ANALYSIS SECTION
        # =================================================================
        st.subheader("Image Analysis")
        with st.expander("Analyze image repair needs"):
            suggestions = analyze_image_repair_type(input_path)
            if suggestions:
                for s in suggestions:
                    st.write(s)
            else:
                st.write("The image appears clean and of good quality.")

        # =================================================================
        # DENOISING METHOD SELECTION
        # =================================================================
        method = st.selectbox(
            "Choose Denoising Method",
            ["Median Filter", "Bilateral Filter", "Non-Local Means", "DnCNN (Deep)", "EDSR"]
        )

        # Optional parameter slider
        strength = 0
        if method == "Bilateral Filter":
            strength = st.slider("Denoising Strength (sigmaColor)", 10, 150, 75)
        elif method == "Non-Local Means":
            strength = st.slider("Denoising Strength (h)", 0.01, 0.2, 0.08, step=0.01)

        # Comparison view mode
        view_mode = st.radio("Compare View", ["Side-by-Side", "Split View"])

        # =================================================================
        # IMAGE REPAIR PROCESS
        # =================================================================
        if st.button("Repair Image"):
            st.write("Processing image, please wait...")

            output_path = os.path.join(repaired_dir, f"repaired_{int(time.time())}.png")

            # Apply selected repair method
            if method == "Median Filter":
                from agents.denoising_median import denoise_image
                denoise_image(input_path, output_path)
            elif method == "Bilateral Filter":
                from agents.denoising_bilateral import denoise_image
                denoise_image(input_path, output_path, sigma_color=strength)
            elif method == "Non-Local Means":
                from agents.denoising_nlmeans import denoise_image
                denoise_image(input_path, output_path, h=strength)
            elif method == "DnCNN (Deep)":
                from agents.dncnn import denoise_image
                denoise_image(input_path, output_path)
            elif method == "EDSR":
                from agents.edsr import edsr_image
                edsr_image(input_path, output_path)

            # =================================================================
            # OUTPUT DISPLAY SECTION
            # =================================================================
            if os.path.exists(output_path):
                repaired_image = Image.open(output_path).convert("RGB")
                st.write(f"Repaired image saved to: {output_path}")

                if view_mode == "Side-by-Side":
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Distorted Image")
                        st.image(image, use_container_width=True)
                    with col2:
                        st.subheader("Repaired Image")
                        st.image(repaired_image, use_container_width=True)
                else:
                    try:
                        from streamlit_image_comparison import image_comparison
                        st.subheader("Compare Using Slider")
                        image_comparison(
                            img1=image,
                            img2=repaired_image,
                            label1="Distorted",
                            label2="Repaired"
                        )
                    except ImportError:
                        st.write("To use split view, install 'streamlit-image-comparison'.")

            else:
                st.write("Repair failed or output image not generated.")

    except Exception as e:
        st.write(f"Error while processing image: {e}")

else:
    st.write("Please upload a .jpg, .jpeg, or .png image to get started.")
