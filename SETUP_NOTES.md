# Docker setup

## To run, run: docker-compose
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

## Apply all pending migrations to the database schema (locally)
`alembic upgrade head`

## Running this from INSIDE the docker container
`docker-compose exec server alembic upgrade head`

## OR running from the machine, but outside the docker container
`DATABASE_URL=postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db alembic upgrade head`

## Generate migration script
`alembic revision --autogenerate -m "baseline schema"`
`docker-compose exec server alembic revision --autogenerate -m "baseline schema"`

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

`alembic show <revision_id>`
`alembic stamp head`
`alembic check`

## Resetting alembic while in development  
- manually delete all versions and generate a baseline schema (with initial command)