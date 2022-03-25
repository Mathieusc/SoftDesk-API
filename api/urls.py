from django.urls import path, include

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import ProjectView, IssueView, AdminProjectViewset

router = routers.SimpleRouter()
router.register("projects", ProjectView, basename="projects")
router.register("issues", IssueView, basename="issues")

router.register("admin/projects", AdminProjectViewset, basename="admin-project")

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
