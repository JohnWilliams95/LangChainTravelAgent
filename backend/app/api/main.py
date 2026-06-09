"""FastAPI主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..config import get_settings, validate_config, print_config
from .routes import trip, poi, map as map_routes
from ..tools.mcp_agent import init_mcp_agent, get_mcp_tools
from ..agents.trip_planner_agent import get_trip_planner_agent
# 获取配置
settings = get_settings()


# 定义lifespan生命周期管理器(on_event方式已被弃用)
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理（替代旧的 on_event）"""
    # --- 启动阶段 (相当于 @app.on_event("startup")) ---
    print("\n" + "="*60)
    print(f"🚀 {settings.app_name} v{settings.app_version}")
    print("="*60)
     # 打印配置信息
    print_config()
    #验证配置
    try:
      validate_config()
      print("\n✅ 配置验证通过")
    except Exception as e:
      print(f"\n❌ 配置验证失败:\n{e}")
      print("\n请检查.env文件并确保所有必要的配置项都已设置")
      raise

    # 初始化MCP Agent（供POI、地图路由使用）
    print("\n🔧 正在初始化MCP Agent...")
    await init_mcp_agent()

    tools = get_mcp_tools()

    get_trip_planner_agent(
      apiKey=settings.openai_api_key,
      baseUrl=settings.openai_base_url,
      modelName=settings.openai_model,
      model_provider=settings.openai_provider,
      tools=tools
    )




    print("\n" + "="*60)
    print("📚 API文档: http://localhost:8000/docs")
    print("📖 ReDoc文档: http://localhost:8000/redoc")
    print("="*60 + "\n")

    # yield分隔startup和shutdown的代码
    yield # yield 之前的代码在应用启动时执行，yield 将控制权交还给框架

    # --- 关闭阶段 (相当于 @app.on_event("shutdown")) ---
    print("\n" + "="*60)
    print("👋 应用正在关闭...")
    print("="*60 + "\n")



# 创建FastAPI应用
app = FastAPI(
  title= settings.app_name,
  version=settings.app_version,
  description="基于HelloAgents框架的智能旅行规划助手API",
  docs_url="/docs",
  redoc_url="/redoc",
  lifespan=lifespan
)

# 配置CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.get_cors_origins_list(),
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# 注册路由
app.include_router(trip.router, prefix="/api")
app.include_router(poi.router, prefix="/api")
app.include_router(map_routes.router, prefix="/api")




@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
   import uvicorn

   uvicorn.run(
      "app.api.main:app",
      host=settings.host,
      port=settings.port,
      reload=True
   )
