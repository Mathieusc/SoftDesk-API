from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterUserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user view with a POST action
    CreateAPIView used for create-only endpoints
    """

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)
