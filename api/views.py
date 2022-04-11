from django.shortcuts import get_object_or_404

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
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
)
from .permissions import (
    IsAuthorProject,
)


class AdminProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]


class ProjectView(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthorProject]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.all()

        # contributor = Contributor.objects.filter(project__in=projects, user=user)
        # projects = Project.objects.filter(contributor_project__in=contributor)

        return projects

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        POST method
        Creation of a project
        fields : title, description, type (author auto create in a contributor object and add to the project)
        return:
        - the created project data with code status 201 if OK
        - the serializer project errors with a status code 400 if not
        """
        project_data = request.data

        serializer = ProjectDetailSerializer(data=project_data, partial=True)
        if serializer.is_valid():
            project = serializer.save()

            contributor = Contributor.objects.create(
                user=self.request.user, project=project, role="AUTHOR"
            )
            contributor.save()

            project.contributor.add(contributor.user)
            project.save()

            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        PUT method
        Modification of a project
        fields : title, description, type
        return: the saved project data with code status 202 ACCEPTED if OK,
        404 NOT FOUND if not found and 403 FORBIDDEN if user is not author, 400 BAD REQUEST
        """

        project = Project.objects.filter(pk=kwargs["pk"])

        project = project.get()

        project_data = request.data
        serializer = ProjectDetailSerializer(data=project_data, partial=True)

        if serializer.is_valid():
            if "title" in project_data:
                project.title = project_data["title"]
            if "description" in project_data:
                project.description = project_data["description"]
            if "type" in project_data:
                project.type = project_data["type"]

            project.save()
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        Deletion of a project
        return : 204 NO CONTENT if ok, 404 NOT FOUND if not found and 403 FORBIDDEN if user is not author
        """
        project = Project.objects.filter(pk=kwargs["pk"])

        project = project.get()
        project.delete()
        return Response(
            {
                "Suppression": f'Suppression du projet {kwargs["pk"]} effectuée avec succès'
            },
            status=status.HTTP_204_NO_CONTENT,
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
