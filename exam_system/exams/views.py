from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg, Max, Min
from django.http import JsonResponse
from .models import Question, Exam, ExamQuestion, ExamResult, StudentAnswer, Subject
from .forms import QuestionForm, ExamForm
from accounts.models import Student


def teacher_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url="accounts:login")(view_func)


def _check_answer(question, selected):
    correct = question.correct_answer
    if question.question_type == "single":
        return bool(selected and selected[0] == correct)
    elif question.question_type == "multiple":
        return bool(set(selected) == set(correct))
    elif question.question_type == "judge":
        return bool(selected and selected[0] == correct)
    return False


# ====== Student ======

@login_required
def exam_list(request):
    exams = Exam.objects.filter(status="published").select_related("subject", "created_by")
    subject_id = request.GET.get("subject")
    if subject_id:
        exams = exams.filter(subject_id=subject_id)

    taken_ids = set()
    if not request.user.is_staff:
        taken_ids = set(ExamResult.objects.filter(student=request.user).values_list("exam_id", flat=True))

    subjects = Subject.objects.all()
    return render(request, "exams/exam_list.html", {
        "exams": exams, "subjects": subjects, "taken_ids": taken_ids,
        "selected_subject": int(subject_id) if subject_id else None,
    })


@login_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, status="published")
    questions = ExamQuestion.objects.filter(exam=exam).select_related("question").order_by("order")

    if not request.user.is_staff:
        if ExamResult.objects.filter(student=request.user, exam=exam).exists():
            return redirect("exams:exam_result", exam_id=exam.id)

    return render(request, "exams/exam_detail.html", {
        "exam": exam, "questions": questions,
        "total_marks": sum(float(q.marks) for q in questions),
    })


@login_required
def take_exam(request, exam_id):
    if request.user.is_staff:
        messages.error(request, "教师账号不能参加考试")
        return redirect("exams:exam_list")

    exam = get_object_or_404(Exam, id=exam_id, status="published")
    eq_list = ExamQuestion.objects.filter(exam=exam).select_related("question").order_by("order")

    if ExamResult.objects.filter(student=request.user, exam=exam).exists():
        messages.warning(request, "你已经参加过本次考试")
        return redirect("exams:exam_result", exam_id=exam.id)

    if request.method == "POST":
        total_score = 0
        correct_count = 0
        wrong_count = 0

        result = ExamResult.objects.create(
            student=request.user, exam=exam, total_marks=exam.total_marks,
        )

        for eq in eq_list:
            q = eq.question
            if q.question_type == "multiple":
                selected = request.POST.getlist(f"question_{q.id}")
            else:
                ans = request.POST.get(f"question_{q.id}", "")
                selected = [ans] if ans else []

            correct = _check_answer(q, selected)
            mark_obtained = float(eq.marks) if correct else 0
            if correct:
                correct_count += 1
            else:
                wrong_count += 1
            total_score += mark_obtained

            StudentAnswer.objects.create(
                result=result, question=q, selected_answer=selected,
                is_correct=correct, marks_obtained=mark_obtained,
            )

        result.score = total_score
        result.correct_count = correct_count
        result.wrong_count = wrong_count
        result.save()

        messages.success(request, f"交卷成功！得分：{total_score}")
        return redirect("exams:exam_result", exam_id=exam.id)

    return render(request, "exams/take_exam.html", {
        "exam": exam, "questions": eq_list, "total_questions": len(eq_list),
    })


@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.user.is_staff:
        results = ExamResult.objects.filter(exam=exam).select_related("student").order_by("-score")
        return render(request, "exams/exam_result.html", {
            "exam": exam, "results": results, "is_teacher_view": True,
        })

    result = ExamResult.objects.filter(student=request.user, exam=exam).first()
    if not result:
        messages.error(request, "你还未参加本次考试")
        return redirect("exams:exam_list")

    answers = StudentAnswer.objects.filter(result=result).select_related("question")
    wrong_answers = [a for a in answers if not a.is_correct]
    stat = {
        "result": result, "answers": answers, "wrong_answers": wrong_answers,
        "correct_count": result.correct_count, "wrong_count": result.wrong_count,
        "total": answers.count(), "passed": result.score >= exam.pass_score,
    }

    return render(request, "exams/exam_result.html", {
        "exam": exam, "stat": stat, "is_teacher_view": False,
    })


@login_required
def wrong_questions(request):
    if request.user.is_staff:
        messages.error(request, "教师账号无需查看错题")
        return redirect("exams:exam_list")

    wrong_answers = StudentAnswer.objects.filter(
        result__student=request.user, is_correct=False
    ).select_related("question", "result__exam").order_by("-result__submitted_at")

    grouped = {}
    for ans in wrong_answers:
        exam_title = ans.result.exam.title
        grouped.setdefault(exam_title, []).append(ans)

    return render(request, "exams/wrong_questions.html", {"grouped": grouped})


# ====== Teacher ======

@login_required
@teacher_required
def question_list(request):
    questions = Question.objects.select_related("subject", "created_by").all()
    subject_id = request.GET.get("subject")
    qtype = request.GET.get("type")
    if subject_id:
        questions = questions.filter(subject_id=subject_id)
    if qtype:
        questions = questions.filter(question_type=qtype)
    subjects = Subject.objects.all()
    return render(request, "exams/question_list.html", {
        "questions": questions, "subjects": subjects,
        "selected_subject": int(subject_id) if subject_id else None,
        "selected_type": qtype,
    })


@login_required
@teacher_required
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.created_by = request.user
            q.save()
            messages.success(request, "题目添加成功")
            return redirect("exams:question_list")
    else:
        form = QuestionForm()
    return render(request, "exams/question_form.html", {"form": form, "editing": False})


@login_required
@teacher_required
def question_edit(request, qid):
    question = get_object_or_404(Question, id=qid)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "题目更新成功")
            return redirect("exams:question_list")
    else:
        form = QuestionForm(instance=question)
    return render(request, "exams/question_form.html", {"form": form, "editing": True})


@login_required
@teacher_required
def question_delete(request, qid):
    get_object_or_404(Question, id=qid).delete()
    messages.success(request, "题目已删除")
    return redirect("exams:question_list")


@login_required
@teacher_required
def exam_manage(request):
    exams = Exam.objects.select_related("subject", "created_by").all()
    return render(request, "exams/exam_manage.html", {"exams": exams})


@login_required
@teacher_required
def exam_create(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, "试卷创建成功，请添加题目")
            return redirect("exams:exam_edit", exam_id=exam.id)
    else:
        form = ExamForm()
    return render(request, "exams/exam_form.html", {"form": form, "editing": False})


@login_required
@teacher_required
def exam_edit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    eqs = ExamQuestion.objects.filter(exam=exam).select_related("question").order_by("order")

    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "试卷信息已更新")
            return redirect("exams:exam_edit", exam_id=exam.id)
    else:
        form = ExamForm(instance=exam)

    available = Question.objects.exclude(
        id__in=eqs.values_list("question_id", flat=True)
    ).select_related("subject")

    return render(request, "exams/exam_edit.html", {
        "form": form, "exam": exam, "questions": eqs,
        "available_questions": available, "editing": True,
    })


@login_required
@teacher_required
def exam_add_question(request, exam_id):
    if request.method != "POST":
        return JsonResponse({"error": "仅支持POST"}, status=405)
    exam = get_object_or_404(Exam, id=exam_id)
    qid = request.POST.get("question_id")
    marks = request.POST.get("marks", 5)
    if not qid:
        return JsonResponse({"error": "缺少题目ID"}, status=400)
    question = get_object_or_404(Question, id=qid)
    if ExamQuestion.objects.filter(exam=exam, question=question).exists():
        return JsonResponse({"error": "该题目已在试卷中"}, status=400)
    max_order = ExamQuestion.objects.filter(exam=exam).aggregate(m=Max("order"))["m"] or 0
    ExamQuestion.objects.create(exam=exam, question=question, marks=marks, order=max_order + 1)
    return JsonResponse({"success": True})


@login_required
@teacher_required
def exam_remove_question(request, exam_id, eq_id):
    eq = get_object_or_404(ExamQuestion, id=eq_id, exam_id=exam_id)
    eq.delete()
    messages.success(request, "题目已移除")
    return redirect("exams:exam_edit", exam_id=exam_id)


@login_required
@teacher_required
def exam_delete(request, exam_id):
    get_object_or_404(Exam, id=exam_id).delete()
    messages.success(request, "试卷已删除")
    return redirect("exams:exam_manage")


@login_required
@teacher_required
def student_manage(request):
    students = Student.objects.select_related("user").all()
    return render(request, "exams/student_manage.html", {"students": students})


@login_required
@teacher_required
def toggle_student_active(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    user.is_active = not user.is_active
    user.save()
    status = "启用" if user.is_active else "禁用"
    messages.success(request, f"账号 {student.student_id} 已{status}")
    return redirect("exams:student_manage")


@login_required
@teacher_required
def statistics(request):
    exam_id = request.GET.get("exam_id")
    subject_id = request.GET.get("subject")
    subjects = Subject.objects.all()

    exams_qs = Exam.objects.all()
    if subject_id:
        exams_qs = exams_qs.filter(subject_id=subject_id)
    if exam_id:
        exams_qs = exams_qs.filter(id=exam_id)

    results = ExamResult.objects.all()
    if exam_id:
        results = results.filter(exam_id=exam_id)
    elif subject_id:
        results = results.filter(exam__subject_id=subject_id)

    total = results.count()
    agg = results.aggregate(avg=Avg("score"), mx=Max("score"), mn=Min("score"))
    avg_score = agg["avg"] or 0
    max_score = agg["mx"] or 0
    min_score = agg["mn"] or 0

    pass_count = sum(1 for r in results.select_related("exam") if r.score >= r.exam.pass_score)
    pass_rate = (pass_count / total * 100) if total > 0 else 0

    exam_stats = Exam.objects.annotate(
        student_count=Count("results"),
        avg_score=Avg("results__score"),
        max_score=Max("results__score"),
    ).filter(student_count__gt=0)
    if subject_id:
        exam_stats = exam_stats.filter(subject_id=subject_id)

    return render(request, "exams/statistics.html", {
        "exams": exams_qs, "exam_stats": exam_stats,
        "total_students": total, "avg_score": round(avg_score, 1),
        "max_score": max_score, "min_score": min_score,
        "pass_count": pass_count, "pass_rate": round(pass_rate, 1),
        "selected_exam": int(exam_id) if exam_id else None,
        "selected_subject": int(subject_id) if subject_id else None,
        "subjects": subjects,
    })