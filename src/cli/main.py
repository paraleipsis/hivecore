import pathlib
import sys

import asyncio
from typing import Annotated

import typer

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from db.database.service import init_models
from auth.utils import generate_secret_key, generate_ssh_keys
from auth.auth_config import CONFIG_FILE, CONFIGS_BASE_DIR
from cli.utils import get_yaml_data, write_yaml_data


cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())


@cli.command()
def secret_key(
        write: Annotated[
            bool,
            typer.Option(
                help="Write generated secret key to configuration file."
            )
        ] = False
):
    """
    Generate Hivecore Secret Key for Authentication purposes.
    """
    key = generate_secret_key()
    if write:
        file = CONFIGS_BASE_DIR / CONFIG_FILE
        data = get_yaml_data(file=file)
        data['SECRET_KEY'] = key
        write_yaml_data(file=file, data=data)
        print(f"Secret key was successfully written to file {file}: {key}")
    else:
        print(f"Secret key: {key}")


@cli.command()
def ssh_keys():
    """
    Generate SSH Public and Private keys for Reverse SSH Client.
    """
    generate_ssh_keys()
    print(f"SSH keys was successfully created")


if __name__ == "__main__":
    cli()
