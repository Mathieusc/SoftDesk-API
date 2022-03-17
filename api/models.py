from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_project"
    )
    # contributor = models.ManyToManyField(User, through="Contributors")

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.user


class Issue(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_issue"
    )
    assignee = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_comments"
    )
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[50:]
