from django.urls import path, include

from rest_framework import routers


from api.views import (
    CommentView,
    ContributorView,
    ProjectView,
    IssueView,
)

router = routers.SimpleRouter()
router.register("projects", ProjectView, basename="projects")

router_2 = routers.SimpleRouter()
router_2.register("users", ContributorView, basename="contributors")
router_2.register("issues", IssueView, basename="issues")

router_3 = routers.SimpleRouter()
router_3.register("comments", CommentView, basename="comments")

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
    path("projects/<int:project_id>/", include(router_2.urls)),
    path("projects/<int:project_id>/issues/<issue_id>/", include(router_3.urls)),
]
