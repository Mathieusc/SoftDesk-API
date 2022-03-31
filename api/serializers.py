from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "priority", "tag", "status", "created_time"]


class IssueDetailSerializer(ModelSerializer):

    # Add in paramater (many=True) if multiple instances
    project = ProjectSerializer()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tag",
            "status",
            "created_time",
            "author",
            "assignee",
            "project",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author", "created_time"]


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "role"]
