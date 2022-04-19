from rest_framework.serializers import ModelSerializer
from .models import Project, Issue, Comment, Contributor


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "role", "project", "user"]


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "contributor"]


class ProjectDetailSerializer(ModelSerializer):
    contributor_project = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "contributor_project"]


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "priority", "tag", "status", "created_time"]


class IssueDetailSerializer(ModelSerializer):
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
            "author_user",
            "assignee",
            "project",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author_user", "issue", "created_time"]
