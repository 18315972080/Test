from django.contrib import admin
from .models import Subject, Question, Exam, ExamQuestion, ExamResult, StudentAnswer


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 5


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "question_count")
    search_fields = ("name",)

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "题目数"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_type", "subject", "content_short", "difficulty", "created_by", "created_at")
    list_filter = ("question_type", "subject", "difficulty")
    search_fields = ("content",)
    list_per_page = 20

    def content_short(self, obj):
        return obj.content[:60]
    content_short.short_description = "题目内容"


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [ExamQuestionInline]
    list_display = ("title", "subject", "duration", "total_marks", "status", "created_by", "created_at")
    list_filter = ("status", "subject")


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "score", "correct_count", "wrong_count", "submitted_at")
    list_filter = ("exam",)
    search_fields = ("student__username",)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("result", "question", "is_correct", "marks_obtained")