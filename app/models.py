from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


class AppVersion(Base):
    __tablename__ = "app_versions"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # ios or android
    version = Column(String, unique=True, index=True)
    version_code = Column(Integer)  # For comparing versions
    download_url = Column(String)
    release_notes = Column(String)
    is_force_update = Column(Boolean, default=False)
    min_required_version = Column(String, nullable=True)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_by_user = relationship("User")


class AppConfig(Base):
    __tablename__ = "app_configs"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)  # 配置项的键名
    value = Column(String)  # 配置项的值
    description = Column(String)  # 配置项的描述
    type = Column(String)  # 配置项的类型（text, color, image, etc.）
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("users.id"))
    visible = Column(Boolean, default=True)  # 配置项是否可见
    created_by_user = relationship("User")
