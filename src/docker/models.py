# from redis_om import JsonModel, EmbeddedJsonModel, Migrator, Field
# from typing import List, Optional
# from uuid import UUID
# from database import redis_connection
#
#
# class DockerNode(EmbeddedJsonModel):
#     name: str
#     node_ip: str
#     environment_id: str = Field(index=True)
#
#     class Meta:
#         database = redis_connection
#
#
# class DockerEnvironment(JsonModel):
#     name: str
#
#     class Meta:
#         database = redis_connection
#
#
# Migrator().run()
