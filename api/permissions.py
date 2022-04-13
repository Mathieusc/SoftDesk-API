from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project, Contributor, Comment, Issue

owner_methods = ("PUT", "DELETE")
contrib_methods = ("POST", "GET")


class IsAuthorProject(BasePermission):
    """
    Access only for project's author
    """

    message = "Vous n'êtes pas auteur du projet. Vous n'avez pas l'autorisation de modifier/supprimer."

    def has_permission(self, request, view):
        if view.action in ["create", "list", "retrieve"]:
            return True
        if view.action in ["update", "destroy"]:
            user = request.user
            if not "project_id" in view.kwargs:
                project_id = view.kwargs["pk"]
            else:
                project_id = view.kwargs["project_id"]
            author = Contributor.objects.filter(
                project=project_id, user=user.id, role="AUTHOR"
            )
            if not author:
                return False


class IsAuthorIssue(BasePermission):
    """
    Access only for Issue's author
    """

    message = "Vous n'êtes pas auteur du problème. Vous n'avez pas l'autorisation de modifier/supprimer."

    def has_permission(self, request, view):
        if view.action in ["create", "list", "retrieve"]:
            return True
        if view.action in ["update", "destroy"]:
            user = request.user
            if not "issue_id" in view.kwargs:
                issue_id = view.kwargs["pk"]
            else:
                issue_id = view.kwargs["issue_id"]
            author = Issue.objects.filter(id=issue_id, author_user=user.id)
            if not author:
                return False
            return True


class IsAuthorComment(BasePermission):
    """
    Access only for Comment's author
    """

    message = "Vous n'êtes pas auteur du problème. Vous n'avez pas l'autorisation de modifier/supprimer."

    def has_permission(self, request, view):
        if view.action in ["create", "list", "retrieve"]:
            return True
        if view.action in ["update", "destroy"]:
            user = request.user
            comment_id = view.kwargs["pk"]
            author = Comment.objects.filter(id=comment_id, author_user=user.id)
            if not author:
                return False
            return True


class IsContributor(BasePermission):
    """
    Access only for project's contributor
    """

    message = "Vous n'êtes pas contributeur du projet. Vous n'avez pas l'autorisation d'y accéder."

    def has_permission(self, request, view):

        user = request.user
        project_id = view.kwargs["project_id"]

        contributor = Contributor.objects.filter(project=project_id, user=user.id)

        if not contributor:
            return False
        else:
            return True


class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if (
            Contributor.objects.filter(user=request.user)
            .filter(project=view.kwargs["project_id"])
            .exists()
        ):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            return obj.author == request.user
        else:
            return False
