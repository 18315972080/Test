from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # 学生端
    path('', views.exam_list, name='exam_list'),
    path('<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('<int:exam_id>/result/', views.exam_result, name='exam_result'),
    path('wrong/', views.wrong_questions, name='wrong_questions'),

    # 教师端 - 题库
    path('questions/', views.question_list, name='question_list'),
    path('questions/create/', views.question_create, name='question_create'),
    path('questions/<int:qid>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:qid>/delete/', views.question_delete, name='question_delete'),

    # 教师端 - 试卷
    path('manage/', views.exam_manage, name='exam_manage'),
    path('manage/create/', views.exam_create, name='exam_create'),
    path('manage/<int:exam_id>/edit/', views.exam_edit, name='exam_edit'),
    path('manage/<int:exam_id>/delete/', views.exam_delete, name='exam_delete'),
    path('manage/<int:exam_id>/add_question/', views.exam_add_question, name='exam_add_question'),
    path('manage/<int:exam_id>/remove_question/<int:eq_id>/', views.exam_remove_question, name='exam_remove_question'),

    # 教师端 - 学生管理
    path('students/', views.student_manage, name='student_manage'),
    path('students/<int:student_id>/toggle/', views.toggle_student_active, name='toggle_student_active'),

    # 教师端 - 统计分析
    path('statistics/', views.statistics, name='statistics'),
]
