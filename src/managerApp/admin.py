from django.contrib import admin
from .models import Teacher


# Register your models here.
class TeacherAdminModel(admin.ModelAdmin):
    # to display columns
    list_display = ["teacher_id", "user"]


admin.site.register(Teacher, TeacherAdminModel)