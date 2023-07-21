![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/7.png)

## Installation

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

## Architecture

![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/1.png)

![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/2.png)

![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/3.png)
