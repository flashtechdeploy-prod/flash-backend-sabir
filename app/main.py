import os
import ssl
import certifi  # Add this if using Option 2
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import fastadmin

from app.core.config import settings
from app.core.database import Base, engine, AsyncSessionLocal
from app.api.routes import api_router
from app.core.startup_tasks import run_startup_tasks
import app.models



# ----------------------------
# FASTAPI APP
# ----------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern ERP system built with FastAPI and React",
)

# ----------------------------
# STARTUP EVENT
# ----------------------------
@app.on_event("startup")
async def startup():
    # Only run database sync if explicitly enabled or locally
    if os.getenv("SYNC_DB_ON_STARTUP", "false").lower() == "true":
        try:
            async with engine.begin() as conn:
                await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, checkfirst=True))
            print("[Startup] Database tables verified/created")
        except Exception as e:
            print(f"[Startup Error] Failed to sync database: {e}")
    
    # Disable startup tasks by default on Vercel
    if os.getenv("RUN_STARTUP_TASKS_ON_STARTUP", "false").lower() == "true":
        try:
            await run_startup_tasks()
            print("[Startup] Startup tasks completed")
        except Exception as e:
            print(f"[Startup Error] Failed to run startup tasks: {e}")

# ----------------------------
# CORS MIDDLEWARE
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list + [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://flash-backend-sabir.vercel.app",
        "https://flash-frontend-sabir.vercel.app",
        "*",  # Allow all as fallback for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ----------------------------
# GLOBAL EXCEPTION HANDLER
# ----------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=500,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true",
        },
    )

# ----------------------------
# ROUTERS
# ----------------------------
app.include_router(api_router, prefix="/api")
app.include_router(fastadmin.api.frameworks.fastapi.app.api_router, prefix="/admin")

# ----------------------------
# UPLOADS (Supabase Storage Only)
# ----------------------------
# All file uploads are now stored in Supabase Storage
# No local file serving needed

# ----------------------------
# ROOT ENDPOINT
# ----------------------------
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        import traceback
        return JSONResponse(
            status_code=500, 
            content={
                "status": "unhealthy", 
                "detail": str(e),
                "traceback": traceback.format_exc()
            }
        )
