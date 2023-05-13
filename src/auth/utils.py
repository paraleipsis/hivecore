import secrets
import asyncssh
from asyncssh import SSHKey

from rssh_client.rssh_config import (SSH_CLIENT_PRIVATE_KEY_PATH, SSH_ALG_NAME, SSH_CLIENT_PUBLIC_KEY_PATH)


def generate_ssh_keys(
        alg_name: str = SSH_ALG_NAME,
        private_key_path: str = SSH_CLIENT_PRIVATE_KEY_PATH,
        public_key_path: str = SSH_CLIENT_PUBLIC_KEY_PATH
) -> SSHKey:
    skey = asyncssh.generate_private_key(alg_name)

    skey.write_private_key(private_key_path)
    skey.write_public_key(public_key_path)

    return skey


def generate_secret_key():
    secret_key = secrets.token_hex(32)

    return secret_key
