from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

from models import (
    Base,
    Product,
    Tag,
    product_tag,
)

from settings import MIGRATION_DB_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    migration_engine = create_engine(MIGRATION_DB_URL, poolclass=pool.NullPool)
    with migration_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
