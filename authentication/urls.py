from django.urls import path
from .views import user_list, user_detail, RegisterView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", user_list),
    path("<int:pk>/", user_detail),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view()),
]
