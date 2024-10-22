# Docker setup

## Just to RUN:
`docker-compose up`

## To BUILD, run: docker-compose
`docker-compose up --build`

## To reset
```
docker-compose down --volumes
docker-compose up --build
```

# Requirements
- Update requirements.in with necessary requirements (no versions)
- use `pip install -r requirements.txt` to update the requirements.txt


# Alembic

## To run any of the commands, but inside the docker container:
`docker-compose exec server YOUR COMMAND`

## Apply all pending migrations to the database schema (locally)
`alembic upgrade head`

## Running this from INSIDE the docker container
`alembic upgrade head`

## Baseline schema command form outside local docker
`DATABASE_URL=postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db alembic revision --autogenerate -m "baseline schema"`

## Upgrade head command from the machine, but outside the docker container
`DATABASE_URL=postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db alembic upgrade head`

## Downgrade through outside docker container
`DATABASE_URL=postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db alembic downgrade -1`


## Generate migration script
`alembic revision --autogenerate -m "baseline schema"`

## Upgrade database to a specifiv revision
`alembic upgrade <revision_id>`

## Reverts schema back to previous version
`Alembic downgrade -1` : downgrades one migration
OR
`alembic downgrade <revision_id>` : downgrades to a revision

## Show the full revision history of migrations
`alembic history`

## Show the current revision applied to the database
`alembic current`

## Other commands
`alembic show <revision_id>`
`alembic stamp head`
`alembic check`

## Resetting alembic while in development  
- manually delete all versions and generate a baseline schema (with reset command)