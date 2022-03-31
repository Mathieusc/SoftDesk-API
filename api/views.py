from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import MultipleChoiceField
from rest_framework.permissions import IsAuthenticated

from authentication.models import User

from .models import Project, Issue, Contributor, Comment
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    ProjectSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
)


class AdminProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]


class ProjectView(ModelViewSet):
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        project = serializer.save()
        Contributor.objects.create(
            user_id=self.request.user, project_id=project, role="Author"
        )


class IssueView(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorView(ModelViewSet):
    serializer_class = ContributorSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contributors = Contributor.objects.filter(project_id=self.kwargs["project_id"])
        return contributors


class CommentView(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comments = Comment.objects.filter(issue_id=self.kwargs["issue_id"])
        return comments
