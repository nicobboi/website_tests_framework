# DEVELOPMENT GUIDE

## Local development requirements

* [Poetry](https://python-poetry.org/) v1.5.1.
* [NodeJS](https://nodejs.org/) v19.6.0.
* [npm](https://docs.npmjs.com/) v9.8.0.

## Dev guide

To use dev configurations, launch `sh docker-compose-dev.sh`: this will launch `docker compose` with `docker-compose.yml` and `docker-compose.dev.yml` as override.

* Now you can open your browser and interact with these URLs:

**Frontend**, React app: http://localhost/

**Backend**, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with **Swagger UI** (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with **ReDoc** (from the OpenAPI backend): http://localhost/redoc

**PGAdmin**, PostgreSQL web administration: http://localhost:5050 (development)

**Flower**, administration of Celery tasks: http://localhost:5555 (development)

**Traefik UI**, to see how the routes are being handled by the proxy: http://localhost:8090

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything, you can check the logs to monitor it.

Now you can start developing: check **[BACKEND](BACKEND.md)** and **[FRONTEND](FRONTEND.md)** for the corresponding framework guide.

Known problems/updates to fix/add are in the [TODO file](../TODO.md).


### Traefik network

This stack expects the public Traefik network to be named `traefik-public`, just as in the tutorials in <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a>.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files, in the section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```

#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.yml` file.

To make sure that your labels are unique per volume per stack (for example, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your `docker-compose.yml` file for the services that need to be fixed with each volume.

To be able to use different environments, like `prod` and `stag`, you should pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME=stag-progetto-com sh ./scripts/deploy.sh
```

To use and expand that environment variable inside the `docker-compose.yml` files you can add the constraints to the services like:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME?Variable not set}.app-db-data == true
```

note the `${STACK_NAME?Variable not set}`. In the script `./scripts/deploy.sh`, the `docker-compose.yml` would be converted, and saved to a file `docker-stack.yml` containing:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.progetto-com.app-db-data == true
```

**Note**: The `${STACK_NAME?Variable not set}` means "use the environment variable `STACK_NAME`, but if it is not set, show an error `Variable not set`".

If you add more volumes to your stack, you need to make sure you add the corresponding constraints to the services that use that named volume.

Then you have to create those labels in some nodes in your Docker Swarm mode cluster. You can use `docker-auto-labels` to do it automatically.

#### `docker-auto-labels`

You can use [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) to automatically read the placement constraint labels in your Docker stack (Docker Compose file) and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

To do that, you can install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

And then run it passing your `docker-stack.yml` file as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.


### Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.

There's a `docker-compose.dev.yml` with overrides for development. It is used by running the shell script `docker-run-dev.sh`.

`docker-compose.build.yml` is used to build and publish the custom images to the repository by github workflows.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

This file is excluded by Git. To create it you have to copy the `.env.template` file and change the configurations.

All the existing default variables are already working, but is suggested to modify them even during development.

