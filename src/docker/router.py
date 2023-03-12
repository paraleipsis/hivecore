# from fastapi import APIRouter, Depends, HTTPException
# from docker.schemas import DockerEnvironmentRead, DockerEnvironmentCreate, DockerNodeCreate, DockerNodeRead
# from docker.models import DockerEnvironment, DockerNode
#
# from typing import List
#
# router = APIRouter(prefix="/docker", tags=["Docker"])
#
#
# @router.get('/environments', response_model=List[DockerEnvironmentRead])
# async def get_all_environments():
#     environments = [DockerEnvironment.get(pk) for pk in DockerEnvironment.all_pks()]
#     return environments
#
#
# @router.post('/environments', response_model=DockerEnvironmentRead)
# async def create_environment(new_environment: DockerEnvironmentCreate):
#     docker_environment = DockerEnvironment(
#         **new_environment.dict()
#     )
#
#     docker_environment.save()
#
#     return docker_environment
#
#
# @router.get('/environments/{env_pk}', response_model=DockerEnvironmentRead)
# async def get_environment(env_pk: str):
#     environment = DockerEnvironment.get(env_pk)
#     return environment
#
#
# @router.delete('/environments/{env_pk}', response_model=bool)
# async def delete_environment(env_pk: str):
#     DockerEnvironment.delete(env_pk)
#     DockerNode.find(DockerNode.environment_id == env_pk).delete()
#     return True
#
#
# @router.get('/environments/{env_pk}/nodes', response_model=List[DockerNodeRead] | None)
# async def get_all_environment_nodes(env_pk: str):
#     nodes = DockerNode.find(DockerNode.environment_id == env_pk).all()
#     return nodes
#
#
# @router.post('/environments/{env_pk}/nodes', response_model=DockerNodeRead)
# async def create_node(env_pk: str, new_docker_node: DockerNodeCreate):
#     docker_node = DockerNode(
#         environment_id=env_pk,
#         **new_docker_node.dict()
#     )
#
#     docker_node.save()
#
#     return docker_node
#
#
# @router.delete('/environments/{env_pk}/nodes/{node_pk}', response_model=bool)
# async def delete_node(env_pk: str, node_pk: str):
#     DockerNode.find(DockerNode.environment_id == env_pk, DockerNode.pk == node_pk).delete()
#
#     return True
#
#
# @router.get('/environments/{env_pk}/nodes/{node_pk}', response_model=DockerNodeRead)
# async def get_environment_node(env_pk: str, node_pk: str):
#     node = DockerNode.find(DockerNode.environment_id == env_pk, DockerNode.pk == node_pk).all()[0]
#
#     return node
