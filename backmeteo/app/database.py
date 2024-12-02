from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword_eee@postgres-container/mydatabase"

# Création du moteur de base de données asynchrone
engine = create_async_engine(DATABASE_URL, echo=True)

# Configuration de la session asynchrone
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dépendance FastAPI pour fournir une session DB
async def get_db():
    async with async_session() as session:
        yield session
