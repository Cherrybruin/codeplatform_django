from django.test import TestCase
from Code_Platform.models import User, ProjectLog, Project, ProjectPermission
from django.contrib.contenttypes.models import ContentType
# Create your tests here.


class UserCreateTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', email='456@456.com', password='456')

    def test_create_user(self):
        self.assertEqual(User.objects.get(username='testuser').username, 'testuser')
        print('create user is  ok')

    def test_delete_user(self):
        User.objects.get(username='testuser').delete()
        print('delete user is ok')


class ProjectCreateTest(TestCase):
    def setUp(self):

        U= User.objects.create(username='123', password='123', email='123@123.com')
        print('create testuser"123" seccess')
        print(User.objects.all())
        PP = ProjectPermission.objects.create(name='Hello World!', content_type=ContentType.objects.get(model='project'),
                                         codename='hello_world')
        P=Project.objects.create(name='Hello World', owner=User.objects.get(username='123'), statue='O')
        print('create testproject group "Hello World" success')
        print('PorjectTesdt setup success')

    def test_create_project(self):
        self.assertEqual(Project.objects.get(name='Hello World').name, 'Hello World')
        print('create project is  ok')

    def test_delete_project(self):
        Project.objects.get(name='Hello World').delete()
        print('delete project is ok')

    def test_set_permission(self):
        Project.objects.get(name='Hello World').permissions.add(ProjectPermission.objects.get(name="Hello World!"))
        print('permission set success')

    def test_user_join_group(self):
        print('user123 group:', User.objects.get(username='123').groups.all())
        User.objects.get(username='123').groups.add(Project.objects.get(name='Hello World'))
        Project.objects.get(name='Hello World').permissions.add(ProjectPermission.objects.get(name="Hello World!"))
        print(ProjectPermission.objects.get(codename='hello_world').content_type.app_label)
        p = ProjectPermission.objects.get(codename='hello_world')
        # print(type(User.objects.get(username='123').get_all_permissions().))
        print('user123 group:', User.objects.get(username='123').groups.all())
        print(User.objects.get(username='123').has_perm(perm=('.'.join([p.content_type.app_label, p.codename]))))
