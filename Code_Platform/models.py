from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    description = models.TextField()
    statue = models.CharField(max_length=5, choices=(
        ('O', 'open'),
        ('B', 'banned'),
        ('C', 'cancel')
    ))


class Project(Group):
    owner = models.ForeignKey(to='User', to_field='username', on_delete=models.CASCADE)
    description = models.TextField()
    statue = models.CharField(max_length=5, choices=(
        ('O', 'open'),
        ('P', 'pause'),
        ('B', 'banned')
    ))

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class ProjectPermission(Permission):
    pass


class ProjectLog(models.Model):
    project = models.ManyToManyField(to=Project,)
    user = models.ManyToManyField(to=User,)
    edit = models.CharField(max_length=5, choices=(
        ('U', 'UPLOAD'),
        ('E', 'EDIT'),
        ('D', 'DELETE')
    ))
    description = models.TextField()
    content = models.TextField()

