
# migration script
`alembic revision --autogenerate -m "baseline schema"`

# Apply all pending migrations to the database schema
`alembic upgrade head`
# or upgrade to a specifiv revision
`alembic upgrade <revision_id>`

# Reverts schema back to previous version
`Alembic downgrade -1` : downgrades one migration
OR
`alembic downgrade <revision_id>` : downgrades to a revision

# Show the full revision history of migrations
`alembic history`

# Show the current revision applied to the database
`alembic current`

`alembic show <revision_id>`
`alembic stamp head`
`alembic check`

# Resetting alembic while in development  
- delete all versions and generate a baseline schema