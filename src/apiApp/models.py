from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # for python 2
    def __unicode__(self):
        return self.user.username

    # for python 3
    def __str__(self):
        return self.user.username


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=15, unique=True)
    dept_id = models.ForeignKey('Department', on_delete=models.CASCADE)

    # for python 2
    def __unicode__(self):
        return self.user.username

    # for python 3
    def __str__(self):
        return self.user.username


class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    # for python 2
    def __unicode__(self):
        return self.name

    # for python 3
    def __str__(self):
        return self.name
