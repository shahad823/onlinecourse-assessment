from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Course, Enrollment, Submission

PASS_PERCENT = 70


def catalog(request):
    return render(request, "onlinecourse/catalog.html", {"courses": Course.objects.order_by("name")})


def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related("lessons", "questions__choices"), pk=course_id
    )
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related("questions__choices"), pk=course_id)
    questions = list(course.questions.all())
    if not questions:
        return redirect("onlinecourse:course_detail", course_id=course.pk)

    selected_choices = []
    results = []
    for question in questions:
        selected_ids = set(request.POST.getlist(f"question_{question.pk}"))
        choices = list(question.choices.all())
        selected = [choice for choice in choices if str(choice.pk) in selected_ids]
        correct = [choice for choice in choices if choice.is_correct]
        is_correct = bool(correct) and selected == correct
        selected_choices.extend(selected)
        results.append({
            "prompt": question.prompt,
            "selected": [choice.text for choice in selected],
            "correct": [choice.text for choice in correct],
            "earned": question.points if is_correct else 0,
            "possible": question.points,
        })

    earned = sum(result["earned"] for result in results)
    possible = sum(result["possible"] for result in results)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    submission = Submission.objects.create(
        enrollment=enrollment,
        earned_points=earned,
        possible_points=possible,
        passed=earned * 100 >= possible * PASS_PERCENT,
        results=results,
    )
    submission.choices.set(selected_choices)
    return redirect("onlinecourse:show_exam_result", course_id=course.pk, submission_id=submission.pk)


@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("enrollment__course"),
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course_id=course_id,
    )
    percent = round(submission.earned_points * 100 / submission.possible_points, 1)
    return render(request, "onlinecourse/exam_result.html", {
        "course": submission.enrollment.course,
        "submission": submission,
        "percent": percent,
        "pass_percent": PASS_PERCENT,
    })
