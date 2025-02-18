from app.database import SessionLocal, Base, engine
from app.models import User
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建表
Base.metadata.create_all(bind=engine)

def create_admin(username: str, password: str, email: str):
    db = SessionLocal()
    # 检查管理员是否存在
    existing_admin = db.query(User).filter(User.username == username).first()
    if existing_admin:
        print("管理员用户已存在")
        db.close()
        return

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
    print("管理员用户创建成功")


if __name__ == "__main__":
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")
    create_admin(username, password, email)
