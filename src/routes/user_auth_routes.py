from fastapi import APIRouter

from src.api.v1.user_authentication.views import user_views
# Add route with prefix /api/v1 to manage v1 APIs.
router = APIRouter(prefix="/api/v1/user-authentication")
router.include_router(user_views.user_api_router, tags=["User Authentication Service Endpoints"])
