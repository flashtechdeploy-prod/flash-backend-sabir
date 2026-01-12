"""API routes package initialization."""

from fastapi import APIRouter

# Core
from app.api.routes.core.auth import router as auth_router
from app.api.routes.core.users import router as users_router
from app.api.routes.core.admin_rbac import router as admin_rbac_router
from app.api.routes.core import upload, bulk, analytics

# Modules
from app.api.routes.client import router as client_management # It was a package
from app.api.routes.fleet import router as fleet_router # Was vehicles
from app.api.routes.fleet import fuel as fuel_entries
from app.api.routes.fleet import assignments as fleet_assignments
from app.api.routes.fleet import maintenance as vehicle_maintenance
from app.api.routes.hr import router as hr_router # Was employees
from app.api.routes.hr.inactive import router as inactive_router
from app.api.routes.hr.payroll import router as payroll_router
from app.api.routes.hr.payroll2 import router as payroll2_router
from app.api.routes.hr.attendance import router as attendance_router
from app.api.routes.hr.leave_periods import router as leave_periods_router
from app.api.routes.hr import analytics_hr
from app.api.routes.hr import advances # Check if this exists
from app.api.routes.inventory import assignments as inventory_assignments
from app.api.routes.inventory import general as general_inventory
from app.api.routes.inventory import restricted as restricted_inventory
from app.api.routes.finance import router as finance_router
from app.api.routes.finance import expenses
from app.api.routes.finance import exports

api_router = APIRouter()

# --- Authentication & Admin (Core) ---
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(admin_rbac_router, prefix="/admin", tags=["Admin"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# --- Core Utilities ---
api_router.include_router(upload.router, prefix="", tags=["Upload"])
api_router.include_router(bulk.router, prefix="/bulk", tags=["Bulk Operations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

# --- Fleet ---
api_router.include_router(fleet_router, prefix="/vehicles", tags=["Fleet"]) # Keep /vehicles prefix for API compatibility? Or change to /fleet? Let's keep /vehicles for now or risk frontend break.
api_router.include_router(fuel_entries.router, prefix="/fuel-entries", tags=["Fuel & Mileage"])
api_router.include_router(fleet_assignments.router, prefix="/vehicle-assignments", tags=["Vehicle Assignments"])
api_router.include_router(vehicle_maintenance.router, prefix="/vehicle-maintenance", tags=["Vehicle Maintenance"])

# --- HR ---
api_router.include_router(hr_router, prefix="/employees", tags=["Employees"])
api_router.include_router(inactive_router, prefix="/employees-inactive", tags=["Inactive Employees"])
api_router.include_router(payroll_router, prefix="/payroll", tags=["Payroll"])
api_router.include_router(payroll2_router, prefix="/payroll2", tags=["Payroll2"])
api_router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(leave_periods_router, prefix="/leave-periods", tags=["Leave Periods"])
# Note: 'advances' was imported from 'employees' before. I assumed it's in hr/router or hr package.
# Let's check where 'advances' is. It was `from app.api.routes.employees import advances`.
# So it should be `from app.api.routes.hr import advances` IF I moved it.
# My move script moved `employees` -> `hr`. So `employees/advances.py` -> `hr/advances.py`.
from app.api.routes.hr import advances
api_router.include_router(advances.router, prefix="/advances", tags=["Accounts & Advances"])
api_router.include_router(analytics_hr.router, prefix="/hr", tags=["HR Analytics"])

# --- Inventory ---
api_router.include_router(inventory_assignments.router, prefix="/inventory-assignments", tags=["Inventory Assignments"])
api_router.include_router(general_inventory.router, prefix="/general-inventory", tags=["General Inventory"])
api_router.include_router(restricted_inventory.router, prefix="/restricted-inventory", tags=["Weapons & Restrict"])

# --- Client ---
api_router.include_router(client_management, prefix="", tags=["Client & Contracts"])

# --- Finance ---
api_router.include_router(exports.router, prefix="/exports", tags=["Exports"])
api_router.include_router(finance_router, prefix="/finance", tags=["Finance"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
