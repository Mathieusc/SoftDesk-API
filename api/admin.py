from django.contrib import admin
from api.models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "author")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)
