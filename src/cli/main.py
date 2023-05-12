import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))

import asyncio

import typer

from db.database.service import init_models

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())


if __name__ == "__main__":
    cli()
