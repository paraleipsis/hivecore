import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

SSH_CLIENT_LOCAL_HOST = os.environ.get("SSH_CLIENT_LOCAL_HOST")
SSH_CLIENT_LOCAL_PORT = os.environ.get("SSH_CLIENT_LOCAL_PORT")
SSH_CLIENT_CLIENT_KEYS = os.environ.get("SSH_CLIENT_CLIENT_KEYS")
SSH_CLIENT_KNOWN_HOSTS = os.environ.get("SSH_CLIENT_KNOWN_HOSTS")
SSH_CLIENT_REUSE_PORT = os.environ.get("SSH_CLIENT_REUSE_PORT")
SSH_CLIENT_MAX_PACKET_SIZE = os.environ.get("SSH_CLIENT_MAX_PACKET_SIZE")
SSH_IDENTIFICATION_URL = os.environ.get("SSH_IDENTIFICATION_URL")
