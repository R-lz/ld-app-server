from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import models, database
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request

# 创建主应用
app = FastAPI(title="App Manager")

# 创建 API 路由器
api_router = FastAPI(title="API Router")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件和模板
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# app.mount("/frontend", StaticFiles(directory="frontend/dist"), name="frontend")
templates = Jinja2Templates(directory="templates")

# 密码加密和JWT配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# 创建上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/version/upload")
async def upload_version(
    platform: str = Form(...),
    version: str = Form(...),
    version_code: int = Form(...),
    release_notes: str = Form(...),
    is_force_update: bool = Form(False),
    min_required_version: Optional[str] = Form(None),
    app_file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 保存文件
    file_location = os.path.join(
        UPLOAD_DIR, f"{platform}_{version}_{app_file.filename}")
    with open(file_location, "wb+") as file_object:
        file_object.write(await app_file.read())

    # 创建新版本记录
    new_version = models.AppVersion(
        platform=platform,
        version=version,
        version_code=version_code,
        download_url=f"/download/{platform}_{version}_{app_file.filename}",
        release_notes=release_notes,
        is_force_update=is_force_update,
        min_required_version=min_required_version,
        created_by=current_user.id
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    return {"status": "success", "version": version}


@app.get("/api/version/check/{platform}")
async def check_version(
    platform: str,
    current_version: str,
    current_version_code: int,
    db: Session = Depends(database.get_db)
):
    latest_version = db.query(models.AppVersion)\
        .filter(models.AppVersion.platform == platform)\
        .order_by(models.AppVersion.version_code.desc())\
        .first()
    if not latest_version:
        return {"has_update": False}
    
    if latest_version.version_code > current_version_code:
        return {
            "has_update": True,
            "latest_version": latest_version.version,
            "download_url": latest_version.download_url,
            "release_notes": latest_version.release_notes,
            "is_force_update": latest_version.is_force_update,
            "min_required_version": latest_version.min_required_version
        }

    return {"has_update": False}


@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/dist/index.html")


@app.get("/api/versions")
async def list_versions(db: Session = Depends(database.get_db)):
    versions = db.query(models.AppVersion).all()
    return versions


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


# 配置管理API
@app.get("/api/configs")
async def list_configs(db: Session = Depends(database.get_db)):
    configs = db.query(models.AppConfig).all()
    return configs

@app.get("/api/configs/{key}")
async def get_config(key: str, db: Session = Depends(database.get_db)):
    config = db.query(models.AppConfig).filter(models.AppConfig.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@app.post("/api/configs")
async def create_config(
    key: str = Form(...),
    value: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    visible: bool = Form(True),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_config = db.query(models.AppConfig).filter(models.AppConfig.key == key).first()
    if existing_config:
        raise HTTPException(status_code=400, detail="Configuration key already exists")
    
    new_config = models.AppConfig(
        key=key,
        value=value,
        description=description,
        type=type,
        created_by=current_user.id,
        visible=visible
    )
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config

@app.put("/api/configs/{key}")
async def update_config(
    key: str,
    value: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    visible: bool = Form(True),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    config = db.query(models.AppConfig).filter(models.AppConfig.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config.value = value
    config.description = description
    config.type = type
    config.visible = visible
    config.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(config)
    return config


@app.on_event("startup")
async def startup_event():
    database.Base.metadata.create_all(bind=database.engine)
