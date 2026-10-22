from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'id']
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','course'],name='unique_course_enrollment')]
    def __str__(self):
        return f'{self.user} - {self.course}'

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=1000)
    grade = models.PositiveIntegerField(default=10)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_submissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions', blank=True)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    @property
    def percentage(self):
        return round(100 * self.score / self.max_score) if self.max_score else 0
    def __str__(self):
        return f'{self.user} - {self.course} - {self.score}/{self.max_score}'
