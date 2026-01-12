from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# --- Determine SSL requirement based on host ---
def _get_connect_args(database_url: str) -> dict:
    """Get connect_args based on database host (SSL only for remote hosts)."""
    try:
        parsed = urlparse(database_url)
        hostname = parsed.hostname or ""
        # Local hosts don't need SSL
        is_local = hostname in ("localhost", "127.0.0.1", "::1") or hostname.startswith("192.168.")
        
        connect_args = {
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
        }
        
        # Only require SSL for remote/cloud databases
        if not is_local:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            connect_args["ssl"] = ctx
        
        return connect_args
    except Exception:
        return {"statement_cache_size": 0, "prepared_statement_cache_size": 0}

# --- Async Setup (for startup tasks and async routes) ---
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args=_get_connect_args(settings.DATABASE_URL),
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

# --- Sync Setup (for existing sync routes) ---
# Translate async URL to sync URL for psycopg2 and strip query params (like ssl=require)
sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
if "?" in sync_url:
    sync_url = sync_url.split("?")[0]

sync_engine = create_engine(
    sync_url,
    echo=False,
    pool_pre_ping=True,
    # Supabase connection pooler works best with some settings
    connect_args={"sslmode": "require"}
)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def get_db():
    """Sync session dependency for standard routes."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Common Setup ---
Base = declarative_base()
