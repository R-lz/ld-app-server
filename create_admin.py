from app.database import SessionLocal, Base, engine
from app.models import User, AppConfig
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
        admin_id = existing_admin.id
    else:
        hashed_password = pwd_context.hash(password)
        admin = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        admin_id = admin.id
        print("管理员用户创建成功")
    
    # 初始化默认配置
    default_configs = [
        {
            "key": "app_secret",
            "value": "your-app-secret-key",
            "description": "APP的秘钥，用于API认证等",
            "type": "text"
        },
        {
            "key": "app_domain",
            "value": "https://example.com",
            "description": "APP的域名配置",
            "type": "text"
        },
        {
            "key": "theme_primary_color",
            "value": "#1890ff",
            "description": "APP的主题主色调",
            "type": "color"
        },
        {
            "key": "theme_secondary_color",
            "value": "#52c41a",
            "description": "APP的主题辅助色",
            "type": "color"
        },
        {
            "key": "home_banner",
            "value": "/static/images/default-home-banner.jpg",
            "description": "首页Banner图片",
            "type": "image"
        },
        {
            "key": "profile_banner",
            "value": "/static/images/default-profile-banner.jpg",
            "description": "个人中心Banner图片",
            "type": "image"
        },
        {
            "key": "app_name",
            "value": "app",
            "description": "APP的名称",
            "type": "text"
        },
            
    ]

    for config in default_configs:
        existing_config = db.query(AppConfig).filter(AppConfig.key == config["key"]).first()
        if not existing_config:
            new_config = AppConfig(
                key=config["key"],
                value=config["value"],
                description=config["description"],
                type=config["type"],
                created_by=admin_id
            )
            db.add(new_config)
            print(f"添加配置: {config['key']}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")
    create_admin(username, password, email)
