from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer, RegisterUserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user view with a POST action
    CreateAPIView used for create-only endpoints
    """

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)


@csrf_exempt  # Be able to POST to this view from clients that won't have a CSRF token
def user_list(request):
    """
    List all users or create a new user.
    """
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=204)
