from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Enrollment, Submission

def course_list(request):
    return render(request,'onlinecourse/course_list.html',{'courses':Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lessons','questions__choices'),pk=course_id)
    return render(request,'onlinecourse/course_details_bootstrap.html',{'course':course})

@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = list(course.questions.prefetch_related('choices').all())
    if not questions:
        messages.error(request,'There are no exam questions for this course yet.')
        return redirect('onlinecourse:course_details',course_id=course.pk)
    selected = []
    score = 0
    for question in questions:
        choice_id = request.POST.get(f'question_{question.pk}')
        choice = question.choices.filter(pk=choice_id).first() if choice_id else None
        if choice is not None:
            selected.append(choice)
            if choice.is_correct:
                score += question.grade
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user,course=course)
    submission = Submission.objects.create(user=request.user,course=course,enrollment=enrollment,score=score,max_score=sum(q.grade for q in questions))
    submission.choices.set(selected)
    return redirect('onlinecourse:show_exam_result',course_id=course.pk,submission_id=submission.pk)

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course,pk=course_id)
    submission = get_object_or_404(Submission,pk=submission_id,course=course,user=request.user)
    chosen_ids = set(submission.choices.values_list('pk',flat=True))
    results = []
    for question in course.questions.prefetch_related('choices').all():
        choices = list(question.choices.all())
        selected_choice = next((c for c in choices if c.pk in chosen_ids),None)
        correct = next((c for c in choices if c.is_correct),None)
        results.append({'question':question,'selected':selected_choice,'correct_choice':correct,'is_correct':bool(selected_choice and selected_choice.is_correct)})
    return render(request,'onlinecourse/exam_result_bootstrap.html',{'course':course,'submission':submission,'results':results,'passed':submission.percentage>=70})
