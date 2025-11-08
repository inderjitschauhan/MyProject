import socket
from pyngrok import ngrok

def get_free_port():
    """Returns a free available port."""
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def kill_ngrok_tunnels():
    """Kills all existing ngrok tunnels."""
    try:
        ngrok.kill()
        print("✅ Ngrok tunnels killed.")
    except Exception as e:
        print(f"⚠️ Could not kill tunnels or none running: {e}")
