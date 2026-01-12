from .router import router, bulk_router

router.include_router(bulk_router)

__all__ = ["router"]
