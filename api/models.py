from django.db import models
from django_project import settings

# Create your models here.
class Project(models.Model):

    BACKEND = "BACK-END"
    FRONTEND = "FRONT-END"
    IOS = "iOS"
    ANDROID = "ANDROID"

    TYPE_CHOICES = [
        (BACKEND, "back-end"),
        (FRONTEND, "front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=128, choices=TYPE_CHOICES, blank=False)
    contributor = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Contributor", related_name="contributions"
    )

    def __str__(self):
        return self.title


class Contributor(models.Model):
    AUTHOR = "AUTHOR"
    CONTRIBUTOR = "CONTRIBUTOR"

    CHOICES = [(AUTHOR, "Auteur"), (CONTRIBUTOR, "Contributeur")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="contributor_project"
    )
    role = models.CharField(max_length=30, choices=CHOICES, verbose_name="role")

    def __str__(self):
        return self.user.email


class Issue(models.Model):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BUG = "BUG"
    IMPROVE = "IMPROVE"
    TASK = "TASK"
    TO_DO = "TO DO"
    IN_PROGRESS = "IN PROGRESS"
    DONE = "DONE"

    PRIORITY_CHOICES = [(LOW, "Faible"), (MEDIUM, "Moyenne"), (HIGH, "Élevée")]

    TAG_CHOICES = [(BUG, "Bug"), (IMPROVE, "Amélioration"), (TASK, "Tâche")]

    STATUS_CHOICES = [(TO_DO, "À faire"), (IN_PROGRESS, "En cours"), (DONE, "Terminé")]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=128, choices=TAG_CHOICES)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author",
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class Comment(models.Model):
    description = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_comments",
    )
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[:50]
