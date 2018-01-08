from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name


# Create your models here.
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # for python 2
    def __unicode__(self):
        return self.user.username

    # for python 3
    def __str__(self):
        return self.user.username


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    dept_id = models.ForeignKey('Department', on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=50, blank=True)    # optional
    academic_yr = models.IntegerField(null=False)   # 2015 -> 2015-16, 2016 -> 2016-2017
    year = models.IntegerField(null=False)  # 1->First Year, 2->Second Year
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    enrollment_complete = models.BooleanField(default=False)

    students = models.ManyToManyField(Student)

    class Meta:
        unique_together = ('name','dept_id', 'academic_yr', 'year', 'teacher_id')

    # for python 2
    def __unicode__(self):
        return self.name

    # for python 3
    def __str__(self):
        return self.name


def course_data_location(instance, filename):
    return "course_models/%s" % (filename)


class CourseData(models.Model):
    data_id = models.AutoField(primary_key=True)
    course_id = models.OneToOneField('Course', on_delete=models.CASCADE)
    data = models.FileField(upload_to=course_data_location)

    # for python 2
    def __unicode__(self):
        return str(self.data_id)

    # for python 3
    def __str__(self):
        return str(self.data_id)


class Lecture(models.Model):
    lect_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    lect_no = models.IntegerField(blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    comment = models.CharField(max_length=50, blank=True)    # optional
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, null=False)
    isAttendanceTaken = models.BooleanField(default=False)

    students = models.ManyToManyField(Student)

    # for python 2
    def __unicode__(self):
        return str(self.lect_id)

    # for python 3
    def __str__(self):
        return str(self.lect_id)


# for class student images
def training_upload_location(instance, filename):
    return "training_data/%s" % (filename)


class StudentData(models.Model):
    data_id = models.AutoField(primary_key=True)
    student_id = models.OneToOneField('Student', on_delete=models.CASCADE)
    data = models.FileField(upload_to=training_upload_location)

    # for python 2
    def __unicode__(self):
        return str(self.data_id)

    # for python 3
    def __str__(self):
        return str(self.data_id)


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=50, null=False)

    # for python 2
    def __unicode__(self):
        return str(self.classroom_id)

    # for python 3
    def __str__(self):
        return str(self.classroom_id)


class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    camera_url = models.CharField(max_length=23, null=False)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)

    # for python 2
    def __unicode__(self):
        return str(self.camera_id)

    # for python 3
    def __str__(self):
        return str(self.camera_id)
