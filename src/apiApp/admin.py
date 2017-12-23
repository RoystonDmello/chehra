from django.contrib import admin
from .models import Teacher, Student, Department


# Register your models here.
class TeacherAdminModel(admin.ModelAdmin):
    # to display columns
    list_display = ["teacher_id", "user"]


class StudentAdminModel(admin.ModelAdmin):
    list_display = ["student_id", "user", "uid", "dept_id"]


class DepartmentAdminModel(admin.ModelAdmin):
    list_display = ["dept_id", "name"]

admin.site.register(Teacher, TeacherAdminModel)
admin.site.register(Student, StudentAdminModel)
admin.site.register(Department, DepartmentAdminModel)
