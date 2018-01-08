from django.contrib import admin
from .models import (
    Teacher, Student,
    Department, Course,
    Lecture, StudentData, CourseData,
    Classroom, Camera
)
from django.contrib.auth import get_user_model
User = get_user_model()


# Register your models here.
class TeacherAdminModel(admin.ModelAdmin):
    # to display columns
    list_display = ["teacher_id", "user"]


class StudentAdminModel(admin.ModelAdmin):
    list_display = ["student_id", "user", "uid", "dept_id"]


class DepartmentAdminModel(admin.ModelAdmin):
    list_display = ["dept_id", "name"]


class CourseAdminModel(admin.ModelAdmin):
    list_display = ["course_id", "dept_id", "teacher_id",
                    "name", "description", "academic_yr", "year",
                    "updated", "created"]

    list_display_links = ["dept_id", "teacher_id"]


class CourseDataAdminModel(admin.ModelAdmin):
    list_display = ['data_id', 'course_id', 'data']


class LectureAdminModel(admin.ModelAdmin):
    list_display = ['lect_id', 'course_id', 'lect_no', 'isAttendanceTaken',
                    'start_time', 'end_time',
                    'comment', 'updated', 'created',
                    'classroom']


class StudentDataAdminModel(admin.ModelAdmin):
    list_display = ['data_id', 'student_id', 'data']


class UserAdminModel(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


class CameraAdminModel(admin.ModelAdmin):
    list_display = ['camera_id', 'camera_url', 'classroom']


class ClassroomAdminModel(admin.ModelAdmin):
    list_display = ['classroom_id', 'classroom_name']

admin.site.register(Teacher, TeacherAdminModel)
admin.site.register(Student, StudentAdminModel)
admin.site.register(Department, DepartmentAdminModel)
admin.site.register(Course, CourseAdminModel)
admin.site.register(CourseData, CourseDataAdminModel)
admin.site.register(Lecture, LectureAdminModel)
admin.site.register(StudentData, StudentDataAdminModel)
admin.site.register(User,UserAdminModel)
admin.site.register(Camera, CameraAdminModel)
admin.site.register(Classroom, ClassroomAdminModel)
