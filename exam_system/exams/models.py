from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    name = models.CharField("科目名称", max_length=50, unique=True)
    class Meta:
        verbose_name = "科目"
        verbose_name_plural = "科目管理"
    def __str__(self):
        return self.name


class Question(models.Model):
    SINGLE = "single"
    MULTIPLE = "multiple"
    TRUE_FALSE = "judge"
    QUESTION_TYPES = [
        (SINGLE, "单选题"),
        (MULTIPLE, "多选题"),
        (TRUE_FALSE, "判断题"),
    ]

    question_type = models.CharField("题型", max_length=10, choices=QUESTION_TYPES, default=SINGLE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目", related_name="questions")
    content = models.TextField("题目内容")
    options = models.JSONField("选项", default=list, blank=True)
    correct_answer = models.JSONField("正确答案")
    difficulty = models.IntegerField("难度", default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    explanation = models.TextField("答案解析", blank=True, default="")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="出题人")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "题目"
        verbose_name_plural = "题库管理"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.content[:50]}"


class Exam(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    FINISHED = "finished"
    STATUS_CHOICES = [
        (DRAFT, "草稿"),
        (PUBLISHED, "已发布"),
        (FINISHED, "已结束"),
    ]

    title = models.CharField("试卷标题", max_length=200)
    description = models.TextField("考试说明", blank=True, default="")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目", related_name="exams")
    duration = models.IntegerField("考试时长（分钟）", default=60, validators=[MinValueValidator(1), MaxValueValidator(600)])
    total_marks = models.DecimalField("总分", max_digits=6, decimal_places=1, default=100)
    pass_score = models.DecimalField("及格分", max_digits=6, decimal_places=1, default=60)
    questions = models.ManyToManyField(Question, through="ExamQuestion", verbose_name="题目")
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建人", related_name="created_exams")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    start_time = models.DateTimeField("开始时间", null=True, blank=True)
    end_time = models.DateTimeField("结束时间", null=True, blank=True)

    class Meta:
        verbose_name = "试卷"
        verbose_name_plural = "试卷管理"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="试卷")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="题目")
    marks = models.DecimalField("分值", max_digits=5, decimal_places=1, default=5)
    order = models.IntegerField("排序", default=0)

    class Meta:
        verbose_name = "试卷题目"
        verbose_name_plural = "试卷题目管理"
        ordering = ["order"]
        unique_together = ("exam", "question")

    def __str__(self):
        return f"{self.exam.title} - {self.question.content[:30]}"


class ExamResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生", related_name="exam_results")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="试卷", related_name="results")
    score = models.DecimalField("得分", max_digits=6, decimal_places=1, default=0)
    total_marks = models.DecimalField("总分", max_digits=6, decimal_places=1, default=0)
    correct_count = models.IntegerField("正确数", default=0)
    wrong_count = models.IntegerField("错误数", default=0)
    submitted_at = models.DateTimeField("提交时间", auto_now_add=True)
    duration_used = models.IntegerField("用时（秒）", default=0)

    class Meta:
        verbose_name = "考试成绩"
        verbose_name_plural = "考试成绩管理"
        ordering = ["-submitted_at"]
        unique_together = ("student", "exam")

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - {self.score}"


class StudentAnswer(models.Model):
    result = models.ForeignKey(ExamResult, on_delete=models.CASCADE, verbose_name="考试结果", related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="题目")
    selected_answer = models.JSONField("学生答案", default=list, blank=True)
    is_correct = models.BooleanField("是否正确", default=False)
    marks_obtained = models.DecimalField("得分", max_digits=5, decimal_places=1, default=0)

    class Meta:
        verbose_name = "答题记录"
        verbose_name_plural = "答题记录管理"
        unique_together = ("result", "question")

    def __str__(self):
        return f"{self.result.student.username} - Q{self.question.id}"