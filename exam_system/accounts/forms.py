from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Teacher


class StudentRegisterForm(UserCreationForm):
    student_id = forms.CharField(label="学号", max_length=20)
    class_name = forms.CharField(label="班级", max_length=50, required=False)
    phone = forms.CharField(label="手机号", max_length=11, required=False)
    email = forms.EmailField(label="邮箱", required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        if commit:
            user.save()
            Student.objects.update_or_create(
                user=user,
                defaults={
                    "student_id": self.cleaned_data["student_id"],
                    "class_name": self.cleaned_data.get("class_name", ""),
                    "phone": self.cleaned_data.get("phone", ""),
                }
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="用户名", max_length=100)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)