from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import settings
from microsoft.db import Base

# NOTE: This line can't be removed as alembic use it for migration control
from microsoft.app.models import *  # isort:skip

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
section = config.config_ini_section
config.set_section_option(section, "DB_USER", settings.DB_USER)
config.set_section_option(section, "DB_PASS", settings.DB_PASS)
config.set_section_option(section, "DB_HOST", settings.DB_HOST)
config.set_section_option(section, "DB_PORT", str(settings.DB_PORT))
config.set_section_option(section, "DB_NAME", settings.DB_NAME)


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == target_metadata.schema
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=settings.build_database_uri(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        version_table_schema=target_metadata.schema,
        include_schemas = True,
        include_name = include_name
    )

    with context.begin_transaction():
        context.execute(f"create schema if not exists {target_metadata.schema};")
        context.execute(f"set search_path to {target_metadata.schema}")
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas = True,
            include_name = include_name
        )

        with context.begin_transaction():
            context.execute(f"create schema if not exists {target_metadata.schema};")
            context.execute(f"set search_path to {target_metadata.schema}")
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
