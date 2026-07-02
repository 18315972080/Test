from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect("exams:exam_list")
    else:
        form = StudentRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("exams:exam_list")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "exams:exam_list")
            return redirect(next_url)
        else:
            messages.error(request, "用户名或密码错误")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    try:
        student = request.user.student_profile
        return render(request, "accounts/profile.html", {
            "student": student, "is_teacher": False,
        })
    except:
        return render(request, "accounts/profile.html", {"is_teacher": True})