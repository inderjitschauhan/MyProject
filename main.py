import os
import threading
import time
import webbrowser
import subprocess
import warnings
from pyngrok import ngrok

from utils.ngrok_utils import get_free_port, kill_ngrok_tunnels
from utils.install_requirements import install_requirements

warnings.filterwarnings("ignore", category=UserWarning)


# ================= Configuration ================= #
NGROK_AUTH_TOKEN = "32YnXNGJ5K3PYpiYrqKQJsB0mXA_7uQ94nt8PEQC9JjRM8Fjb"
APP_PATH = "ui/app.py"

# Mode settings
RUN_EXTERNAL = False         # True: Ngrok public URL, False: Local only
INSTALL_REQUIREMENTS = False # True: Automatically install missing packages
STREAMLIT_HEADLESS = True    # Prevent auto browser launch by Streamlit
STARTUP_DELAY = 5            # Seconds to wait for Streamlit to start
# ================================================== #


def run_streamlit_app(port: int):
    """
    Runs the Streamlit app on the specified port in headless mode.
    """
    cmd = [
        "streamlit", "run", APP_PATH,
        "--server.port", str(port),
        "--server.headless", str(STREAMLIT_HEADLESS).lower()
    ]
    print(f"[INFO] Starting Streamlit app on port {port}...")
    subprocess.run(cmd, shell=False, check=False)


def open_local_app(port: int):
    """
    Opens the Streamlit app locally in the default web browser.
    """
    url = f"http://localhost:{port}"
    print(f"[INFO] Local app running at: {url}")
    webbrowser.open(url)


def open_external_app(port: int):
    """
    Opens the Streamlit app via Ngrok and returns the public URL.
    """
    try:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        public_url = ngrok.connect(addr=port, proto="http").public_url
        print(f"[INFO] External app running at: {public_url}")
        webbrowser.open(public_url)
        return public_url
    except Exception as e:
        print(f"[ERROR] Ngrok tunnel failed: {e}")
        return None


def start_streamlit_thread(port: int):
    """
    Starts Streamlit app in a background daemon thread.
    """
    thread = threading.Thread(target=run_streamlit_app, args=(port,), daemon=True)
    thread.start()
    time.sleep(STARTUP_DELAY)  # wait for app to initialize
    return thread


def main():
    """
    Main execution function.
    Handles port allocation, app startup, and URL opening.
    """
    if INSTALL_REQUIREMENTS:
        install_requirements()

    port = get_free_port()
    print(f"[INFO] Free port found: {port}")

    kill_ngrok_tunnels()

    thread = start_streamlit_thread(port)

    if RUN_EXTERNAL:
        open_external_app(port)
    else:
        open_local_app(port)

    # Keep the script alive until user interrupts
    try:
        while thread.is_alive():
            time.sleep(2)
    except KeyboardInterrupt:
        print("[INFO] Stopping server and cleaning up...")
        kill_ngrok_tunnels()
        print("[INFO] Cleanup complete.")


if __name__ == "__main__":
    main()
