from django.contrib import admin
from Code_Platform.models import User, Project, ProjectPermission, ProjectLog
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectPermission)
admin.site.register(ProjectLog)
