import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.core.base import Base
from app.core.config import settings

from app.core.db import settings  # Импортируем URL базы из db.py


# Настройки логирования Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей
target_metadata = Base.metadata

# Создаем асинхронный движок
connectable = create_async_engine(settings.database_url, poolclass=NullPool)


def run_migrations_offline():
    '''Запуск миграций в офлайн-режиме (без подключения к БД).'''
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    '''Запуск миграций в онлайн-режиме (с подключением к БД).'''
    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    '''Настройка Alembic и запуск миграций.'''
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
