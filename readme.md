# Book Djinni

A personal miniproject to allow my friend and family to conveniently browse my favorite books.

_My plan is to implement this with different stacks (python + fastapi vs graphql + apollo, svelte vs react) to find my favorite combination. This is the python+fastapi version_

- postgres db to store my favorite books and assign them categories, descriptions, comments
- serve and update db-content via fastapi routes, using [SQLModel](https://sqlmodel.tiangolo.com/) to define the DB-schema _and_ the API-data-formats [at the same time](/app/database/models.py)

# deploying

create the requirements from the Pipfile with [jq](https://stedolan.github.io/jq/) like this

$ jq -r '.default  
 | to_entries[]
| .key + .value.version' \
 Pipfile.lock > requirements.txt

## a docker container

$ docker-compose up -d

to start both backend & db in a container

TODO: not sure about the environment variables being loaded from a .env file or whether they are being passed in -> for now its hardcoded

# local development

activate virtualenv
$ pipenv shell

start local db
$ docker-compose up -d djinni_db

create db & seed it

$ python -m database.create
$ python -m database.seed

$ cd app

$ uvicorn main:app --reload --port

# development inside the container [BROKEN]

do a bind mount to have the container be built around the app-directory

-> see docker-compose.yml volume-entry in djinni_backend service -> uncomment ./app:code/app -> not working
