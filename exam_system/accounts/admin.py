from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Teacher


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [StudentInline, TeacherInline]
    list_display = ("username", "email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)