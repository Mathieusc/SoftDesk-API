from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
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
    IsAuthorComment,
    IsAuthorIssue,
    IsContributor,
)


class ProjectView(ModelViewSet):
    """
    GET every projects by the logged in user
    CREATE a new project
    UPDATE a project
    DELETE a project
    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorProject]

    def get_queryset(self):
        """
        GET method
        return: - only the projects assigned to the contributors.
                - if the user is not the author or the contributor the project is not displayed.
        """
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(contributor_project__in=contributor)

        return projects

    def get_serializer_class(self):
        """
        return: the List or the Detail serializer.
        """
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Overwirte POST method
        Create a project.
        The user creating the project is set by default as the author.
        return:
            - If ok -> 201 status code with the created project
            - If not ok -> 400 status code with the error serializer.
        """
        project_data = request.data

        serializer = ProjectDetailSerializer(data=project_data, partial=True)
        if serializer.is_valid():
            project = serializer.save()

            contributor = Contributor.objects.create(
                user=self.request.user, project=project, role="AUTHOR"
            )
            contributor.save()

            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueView(ModelViewSet):
    """
    GET every issues from one project
    CREATE a new issue
    UPDATE an issue
    DELETE an issue
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorIssue, IsContributor]

    def get_queryset(self):
        """
        GET method
        return : every issues from one project
        """
        issues = Issue.objects.filter(project_id=self.kwargs["project_id"])
        return issues

    def get_serializer_class(self):
        """
        return : List or Detail serializer
        """
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        POST Method
        Create an issue to a project.
        The user creating the issue is set by default as the author.
        return :
            if OK --> 201 CREATED
            if data validation is not OK --> 400 BAD REQUEST
        """
        data = request.data
        project_id = kwargs["project_id"]
        author_user = request.user

        if data["assignee"] == "":
            assignee = request.user.id
        else:
            try:
                user = User.objects.get(email=data["assignee"])
                assignee = user.id

            except:
                return Response(
                    {"Assigned user": f"The user {data['assignee']} cannot be found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        new_issue_data = {
            "title": data["title"],
            "description": data["description"],
            "tag": data["tag"],
            "priority": data["priority"],
            "status": data["status"],
            "author_user": author_user.id,
            "project": project_id,
            "assignee": assignee,
        }
        serializer = IssueDetailSerializer(data=new_issue_data, partial=True)
        if serializer.is_valid(project_id):
            new_issue = serializer.save()
            serializer = IssueDetailSerializer(new_issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorView(ModelViewSet):
    """
    GET all contributors from a project
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorProject, IsContributor]

    def get_queryset(self):
        """
        GET method
        return : list of all contributors from a project
        """
        contributors = Contributor.objects.filter(project_id=self.kwargs["project_id"])
        return contributors


class CommentView(ModelViewSet):
    """
    GET all comments from an issue
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorComment, IsContributor]

    def get_queryset(self):
        """
        GET method
        """
        comments = Comment.objects.filter(issue_id=self.kwargs["issue_id"])
        return comments
