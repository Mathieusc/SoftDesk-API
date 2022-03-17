from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]
