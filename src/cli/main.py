import asyncio
from typing import Annotated

import typer

from db.database.service import init_models
from db.broker.service import init_topics
from auth.auth_config import CONFIG_FILE, CONFIGS_BASE_DIR
from cli.utils import (get_yaml_data, write_yaml_data, generate_secret_key, generate_ssh_keys)


cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())


@cli.command()
def broker_init_topics():
    asyncio.run(init_topics())


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
    print("SSH keys was successfully created")


if __name__ == "__main__":
    cli()
