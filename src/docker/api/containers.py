from uuid import UUID

from fastapi import APIRouter

router = APIRouter(
    prefix='/docker/{node_id}',
    tags=['Docker']
)


@router.get(
    '/',
    # response_model=GenericResponseModel[List[schemas_containers.ContainerList]]
)
async def get_docker_node_request(
        node_id: UUID,
):
    # TODO: add Kafka broker query to retrieve host info (each object amount and maybe something else)
    return True
