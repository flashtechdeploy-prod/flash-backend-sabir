from .router import router
from .documents import router as documents_router
from .warnings import router as warnings_router

# Only include sub-routers that belong directly under /employees/{id}/ paths
router.include_router(documents_router)
router.include_router(warnings_router)

# Note: attendance, leave_periods, payroll, payroll2, inactive, and advances
# are mounted separately in app/api/routes/__init__.py with their own prefixes

__all__ = ["router"]
