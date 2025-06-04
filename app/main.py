from pathlib import Path
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .core.dependencies import get_query_token
from .core.db import create_db_and_tables
from .menu.api import ingredients, dishes, kitchenwares


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    # 允许所有来源的跨域请求，你也可以设置为具体的域名来限制请求来源
    allow_origins=["*"],
    # 参数设置为True表示允许携带身份凭证，如cookies
    allow_credentials=True,
    # 表示允许所有HTTP方法的请求
    allow_methods=["*"],
    # 表示允许所有请求头
    allow_headers=["*"],
)

# 挂载静态文件
# 计算前端目录的绝对路径
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

app.include_router(ingredients.router)
app.include_router(dishes.router)
app.include_router(kitchenwares.router)


@app.get("/")
async def read_index():
    return FileResponse(frontend_path / "index.html")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/createdb")
async def create_db():
    create_db_and_tables()
