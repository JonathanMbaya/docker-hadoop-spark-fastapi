from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User

router = APIRouter()

@router.post("/")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "User created", "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute("SELECT * FROM users")
    return {"users": users.fetchall()}
