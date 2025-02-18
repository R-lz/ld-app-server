from app.database import SessionLocal
from app.models import User
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin(username: str, password: str, email: str):
    db = SessionLocal()
    hashed_password = pwd_context.hash(password)
    admin = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.close()


if __name__ == "__main__":
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")
    create_admin(username, password, email)
