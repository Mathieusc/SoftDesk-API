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
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_project",
    )
    # contributor = models.ManyToManyField(User, through="Contributors")

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.user


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

    PRIORITY_CHOICES = [(LOW, "low"), (MEDIUM, "medium"), (HIGH, "high")]

    TAG_CHOICES = [(BUG, "bug"), (IMPROVE, "improve"), (TASK, "task")]

    STATUS_CHOICES = [(TO_DO, "to do"), (IN_PROGRESS, "in progress"), (DONE, "done")]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=128, choices=TAG_CHOICES)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="author_issue",
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING
    )
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_comments",
    )
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[50:]
