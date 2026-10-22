from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help='Create a demo course, lessons, and correctly configured multiple-choice exam.'
    def handle(self,*args,**kwargs):
        course,_=Course.objects.get_or_create(name='Introduction to Django',defaults={'description':'Learn Django models, views, URL routes, templates and assessments.'})
        lessons=[('Django Models','Models describe database tables and relationships.'),('Views and URL Routing','Views process HTTP requests; URL patterns connect paths to views.'),('Templates and Bootstrap','Django templates render dynamic HTML; Bootstrap creates responsive layouts.')]
        for order,(title,content) in enumerate(lessons,1):
            Lesson.objects.update_or_create(course=course,title=title,defaults={'order':order,'content':content})
        questions=[('What is the main purpose of a Django model?',['Manage database data','Style web pages','Start a web server'],0),('Which Django component handles HTTP requests?',['Model','View','Migration'],1),('What is used to render dynamic HTML in Django?',['Template','Admin user','Database index'],0),('What does the {% csrf_token %} template tag protect against?',['CSS errors','Cross-site request forgery','Broken URL paths'],1),('Which command applies Django database migrations?',['python manage.py migrate','python manage.py runserver','python manage.py collectstatic'],0)]
        for question_text,answers,right in questions:
            question,_=Question.objects.update_or_create(course=course,question_text=question_text,defaults={'grade':20})
            for i,answer in enumerate(answers):
                Choice.objects.update_or_create(question=question,choice_text=answer,defaults={'is_correct':i==right})
        self.stdout.write(self.style.SUCCESS(f'Demo course ready: /course/{course.pk}/'))
