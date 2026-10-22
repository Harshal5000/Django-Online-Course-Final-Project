# Django Online Course – Assessment Feature

A working Django app with course/lesson content, multiple-choice exams, graded submissions, a detailed results page, and admin management. Created for the 7-task Online Course final assessment project.

## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/ and log in as the superuser; visit http://127.0.0.1:8000/ to start the course and test the exam. Complete with correct responses to see **Congratulations**, **100%**, and per-question results.

If PowerShell blocks venv activation, use `.\.venv\Scripts\python.exe` instead of `python` for subsequent commands.

## Grading submission map

1. `onlinecourse/models.py` – Question, Choice, Submission.
2. `onlinecourse/admin.py` – seven imported model classes and the four requested admin classes.
3. Capture admin homepage screenshot at `/admin/` as `03-admin-site.png` (Authentication and Authorization and OnlineCourse headings).
4. `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` – course details, lessons and exam form.
5. `onlinecourse/views.py` – submit and show_exam_result.
6. `onlinecourse/urls.py` – submission/result routes.
7. Capture successful completed exam result screen as `07-final.png`.

**Do not submit invented screenshots:** capture them from the running application. Do not commit `.env`, `db.sqlite3`, virtual environments, or passwords. Bootstrap uses a CDN, so internet access is needed for styling. This starter uses Django's development server and is not configured for production hosting.
