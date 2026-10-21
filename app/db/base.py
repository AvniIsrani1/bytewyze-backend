# Import every table model here so Alembic can see it.
# Adding a table? Add one import line below, then create a migration.
from app.models.user import User  # noqa: F401
