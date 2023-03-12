# from pydantic import BaseModel
#
#
# class DockerEnvironmentRead(BaseModel):
#     pk: str
#     name: str
#
#     class Config:
#         orm_mode = True
#
#
# class DockerEnvironmentCreate(BaseModel):
#     name: str
#
#
# class DockerNodeRead(BaseModel):
#     pk: str
#     name: str
#     node_ip: str
#
#     class Config:
#         orm_mode = True
#
#
# class DockerNodeCreate(BaseModel):
#     name: str
#     node_ip: str
