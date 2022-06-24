from django.contrib import admin
from api.models import Project, Issue, Comment, Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "type")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "priority",
        "tag",
        "status",
        "author_user",
        "assignee",
        "project",
    )


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "role")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "author_user", "issue")
