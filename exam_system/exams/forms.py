from django import forms
from .models import Question, Exam, Subject


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question_type", "subject", "content", "options", "correct_answer",
                  "difficulty", "explanation")
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "explanation": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "options": forms.Textarea(attrs={"rows": 4, "class": "form-control",
                                              "placeholder": "每行一个选项，如：\nA. 选项内容\nB. 选项内容\nC. 选项内容\nD. 选项内容"}),
            "correct_answer": forms.TextInput(attrs={"class": "form-control",
                                                      "placeholder": "单选题填 A/B/C/D；多选题填 A,B；判断题填 正确/错误"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "question_type": forms.Select(attrs={"class": "form-select"}),
            "difficulty": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
        }
        labels = {
            "question_type": "题型", "subject": "科目", "content": "题目内容",
            "options": "选项", "correct_answer": "正确答案", "difficulty": "难度 (1-5)",
            "explanation": "答案解析",
        }

    def clean_options(self):
        data = self.cleaned_data["options"]
        if isinstance(data, str):
            lines = [line.strip() for line in data.strip().split("\n") if line.strip()]
            return lines
        return data

    def clean_correct_answer(self):
        data = self.cleaned_data["correct_answer"]
        if isinstance(data, str):
            qtype = self.cleaned_data.get("question_type")
            if qtype == "multiple":
                return [a.strip() for a in data.split(",") if a.strip()]
            return data.strip()
        return data


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ("title", "description", "subject", "duration", "total_marks",
                  "pass_score", "status", "start_time", "end_time")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "duration": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "total_marks": forms.NumberInput(attrs={"class": "form-control"}),
            "pass_score": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "start_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }
        labels = {
            "title": "试卷标题", "description": "考试说明", "subject": "所属科目",
            "duration": "考试时长（分钟）", "total_marks": "总分", "pass_score": "及格分",
            "status": "状态", "start_time": "开始时间", "end_time": "结束时间",
        }