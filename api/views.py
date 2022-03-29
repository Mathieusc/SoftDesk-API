from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import MultipleChoiceField
from rest_framework.permissions import IsAuthenticated

from .models import Project, Issue, Contributor
from .serializers import ProjectSerializer, IssueListSerializer, IssueDetailSerializer


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
            user_id=self.request.user, project_id=project, role="Créateur"
        )


class IssueView(ReadOnlyModelViewSet):
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
