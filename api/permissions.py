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
            return True


# class HasProjectPermission(BasePermission):
#     def has_permission(self, request, view):
#         if (
#             Contributor.objects.filter(user=request.user)
#             .filter(project=view.kwargs["project_id"])
#             .exists()
#         ):
#             return True
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         if request.method in owner_methods:
#             return obj.author == request.user
#         else:
#             return False


# class HasContributorPermission(BasePermission):
#     def has_permission(self, request, view):
#         project = Project.objects.get(id=view.kwargs["project_id"])
#         if project in Project.objects.filter(contributors__user=request.user):
#             project = Project.objects.get(id=view.kwargs["project_id"])
#             if request.method in SAFE_METHODS:
#                 return True
#             return request.user == project.author
#         return False


# class HasIssuePermission(BasePermission):
#     def has_permission(self, request, view):
#         if (
#             Contributor.objects.filter(user=request.user)
#             .filter(project=view.kwargs["project_id"])
#             .exists()
#         ):
#             return True
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         if request.method in owner_methods:
#             if obj.author == request.user:
#                 return True
#         else:
#             return request.user == obj.author


# class HasCommentPermission(BasePermission):
#     def has_permission(self, request, view):
#         if (
#             Contributor.objects.filter(user=request.user)
#             .filter(project=view.kwargs["project_id"])
#             .exists()
#         ):
#             return True

#     def has_object_permission(self, request, view, obj):
#         if request.method in owner_methods:
#             if obj.author == request.user:
#                 return True
#         else:
#             return request.user == obj.author
