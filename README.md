![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/7.png)

## Overview

This is a RESTful API for remote Docker and Swarm resources management built with FastAPI, PostgreSQL, Kafka, Aiohttp, AsyncSSH and providing the following functionality:

- Hosts registration and authentication system based on JWT strategy. It provides the ability to perform CRUD operations with hosts. JWT token contains the IP address of the server to connect to and the public RSA key for the SSH tunnel. The [host-agent](https://github.com/paraleipsis/hivecore-agent) (for local management on target host) automatically decode this data from the token and uses it
- An application to perform CRUD operations with clusters. Creation of clusters in the server database and adding hosts to these clusters performs manually. This application does not affect the actual location of the host in the Swarm cluster. Data on whether the host belongs to a particular cluster (nor is its creation) is not automatically entered into the database
- Connection to remote host-agents based on reverse SSH tunnel. This provides the ability to connect to hosts in different networks. After deployment, the agent itself establishes a connection with the server, then they change places in the client-server model so that the server can send requests to the remote agent and manage Docker and Swarm resources. This functionality is provided by a separate module built on [rrssh framework](https://github.com/paraleipsis/rrssh) and used as a proxy service. This service runs as a background FastAPI server task. Host authentication occurs at the stage of receiving a request by a proxy service, where it sends a request to the server at /api/nodes/auth with host data. All further communication between the API server and the host-agent is done through a proxy service which is running on both the server and the agent
- Checking if Docker is running after a connection is established and if the Swarm cluster is active. The status of being in a Swarm cluster is updated in real time
- An application for monitoring and collecting data from hosts on the server after a new connection establishes a persistent TCP connection through its rrssh proxy to the proxy service of the host agent, passing the necessary endpoint for direct access to the aiohttp server of the host agent. The agent proxy service establishes a WebSocket connection to the received endpoint (/report/snapshot/docker) of aiohttp server to collect snapshots of the current state of the Docker and Swarm resources of the host. A resources snapshot is created and sent every time an event occurs in the Docker Engine. It turns out that host resources data is transmitted through one persistent connection as soon as it is updated. The server sends the received host snapshot to the Kafka broker
- All data about host resources can be obtained both from the server WebSocket endpoint and a single GET request
- Ability to directly manage and configure Docker and Swarm resources on a remote host
- Scaling platform components: Kafka, PostgreSQL. The API server cannot be scaled horizontally at the moment due to the stateful state (SSH connection with hosts) - it will be resolved soon

## Features

- Hosts authentication
- Swarm multicluster management
- Real-time host telemetry
- Secure connection with hosts based on reverse SSH tunnel
- Docker and Swarm resources management on hosts
- Remote hosts support (Edge)

## Installation

- Install Docker
- Clone this repository and navigate to it:
  
```bash
git clone https://github.com/paraleipsis/hivecore.git && cd hivecore
```

- Run services with Docker Compose:

```bash
docker compose up -d
```

Swagger UI documentation by default will be available at: <http://localhost:8003/api/docs>

Open API documentation by default will be available at: <http://localhost:8003/api/openapi.json>

## Add a remote/local Docker/Swarm host using Hivecore Agent

- Register a new host at /api/nodes/. As a request body it optionally accepts a host name, its description, and the expiration date of the JWT token (default 0 - infinite). The required parameter is the IP address of the server to which the host-agent will connect. The response will return the UUID of the host and its JWT token
- Deploy the [host-agent](https://github.com/paraleipsis/hivecore-agent) by specifying the UUID and JWT token in the agent configuration /configs/agent_config.yml

## Configuration 

Authentication:

```bash
nano configs/auth_config.yml
```

Logging:

```bash
nano src/logger/logger_config.yml
```

API server:

```bash
nano configs/core_config.yml
```

PostgreSQL and Kafka:

```bash
nano configs/storage_config.yml
```

Reverse SSH proxy client:

```bash
nano configs/rssh_client_config.yml
```

## Platform components

![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/4.png)
