from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

# importing base registers every table model with SQLModel.metadata
import app.db.base  # noqa: F401
from app.db.session import get_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """No database connection: prints the SQL instead of running it (alembic upgrade head --sql)."""
    context.configure(
        dialect_name="mysql",
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Runs against the real database, using the same engine as the app (.env settings + TLS)."""
    with get_engine().connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
