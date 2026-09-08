from fastapi import FastAPI 
from app.routers import auth 
from app.routers import team
from app.routers import user
from app.models.users import User
from app.core.database import engine , Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(team.router)
app.include_router(user.router)

