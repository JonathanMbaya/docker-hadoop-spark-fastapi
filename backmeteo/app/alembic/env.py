from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from app.database import Base  # Importez votre Base ici

import os

# Ce fichier de configuration d'Alembic
config = context.config
fileConfig(config.config_file_name)

# Configuration de la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://myuser:mypassword_eee@postgres-container/mydatabase"
)
target_metadata = Base.metadata

def run_migrations_offline():
    """Exécution des migrations en mode hors ligne."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécution des migrations en mode en ligne."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
