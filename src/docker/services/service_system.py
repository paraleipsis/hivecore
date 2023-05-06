from typing import Generator, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.broker.broker import consume
from db.config import DOCKER_KAFKA_TOPIC
from docker.crud.crud_system import (get_docker_system_info, get_docker_system_df, get_docker_version)
from docker.client.client_system import (docker_login, docker_events, prune_system)
from docker.schemas.schemas_system import (SystemDF, SystemVersion, SystemInfo)
from modules.rssh.client.client import ReverseSSHClient
from modules.schemas.schemas_docker_snapshot import DockerSnapshot
from modules.schemas.schemas_response import GenericResponseModel
from modules.utils.utils import is_equal


async def get_system_info_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[SystemInfo]:
    crud_system = await get_docker_system_info(
        node_id=node_id,
        session=session
    )

    return GenericResponseModel(
        data=crud_system.dict(),
    )


async def get_system_df_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[SystemDF]:
    crud_df = await get_docker_system_df(
        node_id=node_id,
        session=session,
    )

    return GenericResponseModel(
        data=crud_df.dict(),
    )


async def get_docker_version_from_db(
        node_id: UUID,
        session: AsyncSession
) -> GenericResponseModel[SystemVersion]:
    crud_version = await get_docker_version(
        node_id=node_id,
        session=session,
    )

    return GenericResponseModel(
        data=crud_version.dict(),
    )


async def get_system_info_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[SystemInfo],
    GenericResponseModel[SystemInfo],
    None
]:
    info_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            info = snapshot.docker.system

            if not is_equal(old_object=info_data, new_object=info.data):
                info_data = info.data

                yield GenericResponseModel(
                    data=info.data
                )


async def get_system_df_from_broker(
        node_id: UUID,
) -> Generator[
    GenericResponseModel[SystemDF],
    GenericResponseModel[SystemDF],
    None
]:
    df_data = ''
    async for message in consume(topic=DOCKER_KAFKA_TOPIC):
        if message.key == str(node_id):
            snapshot = DockerSnapshot(**message.value)
            df = snapshot.docker.df

            if not is_equal(old_object=df_data, new_object=df.data):
                df_data = df.data

                yield GenericResponseModel(
                    data=df.data
                )


async def check_auth_conf(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await docker_login(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def prune_docker_system(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
        **kwargs
) -> GenericResponseModel:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']
    response = await prune_system(
        ssh_session=host_ssh_session,
        **kwargs
    )

    response_obj = GenericResponseModel(**response['response'])

    return response_obj


async def get_docker_events(
        host_uuid: UUID,
        rssh_client: ReverseSSHClient,
) -> Generator[Dict, Dict, None]:
    host_ssh_session = rssh_client.get_connection(host_uuid=host_uuid)['session']

    async for msg in docker_events(
            ssh_session=host_ssh_session
    ):
        event = msg['response']
        yield event
