from fastapi import APIRouter

from src.api.v1.employee_recognition.views import views as employee_views

# Add route with prefix /api/v1 to manage v1 APIs.
router = APIRouter(prefix="/api/v1/user-recognition")
router.include_router(employee_views.employee_router, tags=["Employee Recognition Service Endpoints"])
