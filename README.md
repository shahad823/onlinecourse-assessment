# OnlineCourse assessment

A Django course catalog and mock assessment. Learners sign in, view lessons, submit a multiple-choice exam, and review their score and answers. Each question earns full credit when the selected options match all its correct choices. The pass threshold is 70%.

## Run locally

With Python 3.10 or later, run these commands in the project directory.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the course. The account you just created can sign in to the course and to http://127.0.0.1:8000/admin/. Use the demo course's lessons to complete the mock exam.

## Submission files

| Question | File |
| --- | --- |
| 1 | `onlinecourse/models.py` |
| 2 | `onlinecourse/admin.py` |
| 3 | `03-admin-site.png` from the admin dashboard |
| 4 | `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | `onlinecourse/views.py` |
| 6 | `onlinecourse/urls.py` |
| 7 | `07-final.png` from the successful exam attempt |

Questions 1, 2, 4, 5, and 6 expect direct public GitHub links to the corresponding source files.
