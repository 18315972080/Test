from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField("学号", max_length=20, unique=True)
    class_name = models.CharField("班级", max_length=50, blank=True)
    phone = models.CharField("手机号", max_length=11, blank=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生管理"

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name() or self.user.username}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    teacher_id = models.CharField("工号", max_length=20, unique=True)
    department = models.CharField("院系", max_length=50, blank=True)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = "教师管理"

    def __str__(self):
        return f"{self.teacher_id} - {self.user.get_full_name() or self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff or instance.is_superuser:
            Teacher.objects.get_or_create(
                user=instance,
                defaults={"teacher_id": f"T{instance.id:06d}"}
            )
        else:
            Student.objects.get_or_create(
                user=instance,
                defaults={"student_id": f"S{instance.id:06d}"}
            )