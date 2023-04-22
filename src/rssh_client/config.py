import os

from dotenv import load_dotenv

load_dotenv()

SSH_CLIENT_LOCAL_HOST = os.environ.get("SSH_CLIENT_LOCAL_HOST")
SSH_CLIENT_LOCAL_PORT = os.environ.get("SSH_CLIENT_LOCAL_PORT")
SSH_CLIENT_CLIENT_KEYS = os.environ.get("SSH_CLIENT_CLIENT_KEYS")
SSH_CLIENT_KNOWN_HOSTS = os.environ.get("SSH_CLIENT_KNOWN_HOSTS")
SSH_CLIENT_REUSE_PORT = os.environ.get("SSH_CLIENT_REUSE_PORT")
SSH_CLIENT_MAX_PACKET_SIZE = os.environ.get("SSH_CLIENT_MAX_PACKET_SIZE")
