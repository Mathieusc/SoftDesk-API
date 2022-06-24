from rest_framework.permissions import BasePermission
from .models import Contributor, Comment, Issue


class IsAuthorProject(BasePermission):
    """
    Author's project permissions:
        - Only the author can update or delete a project.
    """

    message = "Only the author can update or delete a project."

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            project_id = view.kwargs["pk"]
            user_id = request.user.id
            author = Contributor.objects.filter(
                project=project_id, user=user_id, role="AUTHOR"
            )
            if not author.exists():
                return False
        return True


class IsAuthorIssue(BasePermission):
    """
    Author's issue permissions:
        - Only the author can update or delete an issue
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            user = request.user
            issue_id = view.kwargs["pk"]
            author = Issue.objects.filter(id=issue_id, author_user=user.id)
            if not author.exists():
                return False
        return True


class IsAuthorComment(BasePermission):
    """
    Author's comments permissions:
        - Only the author of a comment can update or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            user = request.user
            comment_id = view.kwargs["pk"]
            author = Comment.objects.filter(id=comment_id, author_user=user.id)
            if not author.exists():
                return False
        return True


class IsContributor(BasePermission):
    """
    Contributors permissions:
        - The contributors can only read and create issues or comments if they are assigned to the project.
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs["project_id"]

        contributor = Contributor.objects.filter(project=project_id, user=user.id)
        if request.method in ["GET", "POST"]:
            if not contributor.exists():
                return False
        return True
