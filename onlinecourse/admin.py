from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Question, Choice, Submission
# Seven imported model classes: User, Course, Lesson, Enrollment, Question, Choice, Submission.

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','course','lesson','grade')
    list_filter = ('course',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title','course','order')
    list_filter = ('course',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [QuestionInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text','question','is_correct')
    list_filter = ('is_correct',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','course','enrolled_at')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user','course','score','max_score','submitted_at')
    filter_horizontal = ('choices',)
    readonly_fields = ('score','max_score','submitted_at')
