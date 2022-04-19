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
from .permissions import IsAuthorProject, IsAuthorIssue, IsAuthorComment, IsContributor


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
        return: every projects by the logged in user
        """
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(contributor_project__in=contributor)

        return projects

    def get_serializer_class(self):
        """
        return: the List OR de Detail serializer
        """
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        POST method
        Create a project
        fields : id, title, description, type, contributor (author is auto-created)
        return:
        - the created project data with the status code 201 if OK
        - the serializer project errors with the status code 400 if not
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

    def update(self, request, *args, **kwargs):
        """
        PUT method
        Update a project
        fields : title, description, type
        return: the saved project data with code status 202 ACCEPTED if OK,
        400 BAD REQUEST if not
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
        Deletes a project
        return : 204 NO CONTENT if ok
        """
        project = Project.objects.filter(pk=kwargs["pk"])

        project = project.get()
        project.delete()
        return Response(
            {"Suppression": f'Projet {kwargs["pk"]} supprimé.'},
            status=status.HTTP_204_NO_CONTENT,
        )


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
        queryset = Issue.objects.all()
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

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
        Create an issue to a project. Author of the issue is auto-created.
        fields : title, description, tag, priority, status, assignee_user
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
                    {
                        "Utilisateur assigné": f"L'utilisateur {data['assignee']} est introuvable."
                    },
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

    def update(self, request, *args, **kwargs):
        """
        PUT Method
        Update an issue of a project.
        fields : title, description, tag, priority, status, assignee_user
        return :
        if OK --> 202 accepted
        if data validation is not OK --> 400 BAD REQUEST
        """
        issue = Issue.objects.filter(pk=kwargs["pk"])

        issue = issue.get()
        issue_data = request.data
        data = {}

        if "description" in issue_data:
            issue.description = issue_data["description"]
            data["description"] = issue_data["description"]
        if "tag" in issue_data:
            issue.tag = issue_data["tag"]
            data["tag"] = issue_data["tag"]
        if "priority" in issue_data:
            issue.priority = issue_data["priority"]
            data["priority"] = issue_data["priority"]
        if "status" in issue_data:
            issue.status = issue_data["status"]
            data["status"] = issue_data["status"]

        serializer = IssueDetailSerializer(data=data, partial=True)

        if serializer.is_valid():

            issue.save()
            serializer = IssueDetailSerializer(issue)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        DELETE an issue from a project.
        return :
        if OK --> 204 NO CONTENT
        if issue doesn't exist --> 404 NOT FOUND
        """
        issue = Issue.objects.filter(pk=kwargs["pk"])
        if not issue:
            return Response(
                {"Issue": f"Le problème {kwargs['pk']} est introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        issue = issue.get()
        issue.delete()
        return Response(
            {"Suppression": f'Problème {kwargs["pk"]} supprimé.'},
            status=status.HTTP_204_NO_CONTENT,
        )


class ContributorView(ModelViewSet):
    """
    GET all contributors from a project
    ADD a new contributor
    DELETE a contributor
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

    def create(self, request, *args, **kwargs):
        """
        POST Method
        Add a new contributor to a project : may be a CONTRIBUTOR or an AUTHOR. Multi author is allowed.
        fields : user, project, role
        return :
        if not AUTHOR of the project --> 403 FORBIDDEN
        if user doesn't exist in the base --> 404 not found
        if user is already a contributor of the project --> 400 BAD REQUEST
        if errors in the data fields --> 400 BAD REQUEST
        if OK --> 201 CREATED
        """

        author = Contributor.objects.filter(
            project_id=self.kwargs["project_id"], user=request.user.id, role="AUTHOR"
        )
        if not author:
            return Response(
                {"detail:": "Seul l'auteur peut modifier/supprimer un projet."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        user_email = data["user"]

        user_object = User.objects.filter(email=user_email)
        for user in user_object:
            user_id = user.id
        if not user_object:
            return Response(
                {"Utilisateur": f"{user_email} est introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            project_id = kwargs["project_id"]
            role = data["role"]

            contributor = Contributor.objects.filter(project=project_id, user=user_id)
            if contributor:
                return Response(
                    {
                        "Contributor:": "Cet utilisateur est déjà contributeur du projet."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:

                data = {
                    "project": project_id,
                    "role": role,
                    "user": user_id,
                }

                serializer = ContributorSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        delete a contributor from a project
        return :
        if not AUTHOR of the project --> 403 FORBIDDEN
        if user doesn't exist in the base --> 404 not found
        if OK --> 204 NO CONTENT
        """
        try:
            delete_user = Contributor.objects.get(pk=kwargs["pk"])
            delete_user.delete()

            return Response(
                {
                    "Suppression": f'Contributeur {kwargs["pk"]} du projet '
                    f'{kwargs["project_id"]} supprimé.'
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except:
            return Response(
                {
                    "Contributeur": f"L'utilisateur {kwargs['pk']} du projet {kwargs['project_id']} est introuvable."
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class CommentView(ModelViewSet):
    """
    GET all comments from an issue
    GET comment's details with its ID
    CREATE a new comment
    UPDATE a comment
    DELETE a comment
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorComment, IsContributor]

    def get_queryset(self):
        """
        GET method
        return : all comments from an issue
        """
        comments = Comment.objects.filter(issue_id=self.kwargs["issue_id"])
        return comments

    def create(self, request, *args, **kwargs):
        """
        POST Method
        create a new comment for an issue. Author is automatically the user who created the issue,
        issue is automatically completed
        fields : description
        returns :
        if no description (in body or in data) --> 400 BAD REQUEST
        if OK --> 201 CREATED
        """
        data = request.data

        if not "description" in data:
            return Response(
                {
                    "description": "Le couple clef / valeur 'description' doit être renseigné dans la partie 'body'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CommentSerializer(data=data, partial=True)

        if serializer.is_valid():
            comment_data = {}
            author_user = request.user
            issue = Issue.objects.get(pk=kwargs["issue_id"])

            comment_data["author_user"] = author_user.id
            comment_data["issue"] = issue.id
            comment_data["description"] = data["description"]

            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        PUT Method
        Update a comment
        fields : description
        returns :
        if no description (in body or in data) --> 400 BAD REQUEST
        if OK --> 202 ACCEPTED
        """
        data = request.data
        if not "description" in data:
            return Response(
                {
                    "description": "Le couple clef / valeur 'description' doit être renseignée dans la partie 'body'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = Comment.objects.filter(pk=kwargs["pk"])

        comment = comment.get()
        serializer = CommentSerializer(data=data, partial=True)
        if serializer.is_valid():
            comment.description = data["description"]
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        deletes a comment
        return :
        if comment doesn't exist --> 404 NOT FOUND
        if comment's author != user --> 403 FORBIDDEN
        if OK --> 204 NO CONTENT
        """
        comment = Comment.objects.filter(pk=kwargs["pk"])

        comment = comment.get()
        comment.delete()
        return Response(
            {
                "Suppression": f'Suppression du commentaire {kwargs["pk"]} du problème '
                f'{kwargs["issue_id"]} effectuée avec succès'
            },
            status=status.HTTP_204_NO_CONTENT,
        )
