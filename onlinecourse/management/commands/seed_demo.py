from django.core.management.base import BaseCommand
from django.db import transaction

from onlinecourse.models import Choice, Course, Instructor, Lesson, Question


class Command(BaseCommand):
    help = "Create the sample course, lessons, and mock exam."

    @transaction.atomic
    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Django Fundamentals",
            defaults={"description": "Learn how Django connects data, templates, and requests."},
        )
        instructor, _ = Instructor.objects.get_or_create(name="Demo Instructor")
        course.instructors.add(instructor)
        examples = [
            (
                "Models and data", "Models describe the data stored by an application and its relationships.",
                "Which component defines database-backed data?", 2,
                [("A model", True), ("A template", False), ("A stylesheet", False)],
            ),
            (
                "URLs and views", "URL patterns route incoming requests to views, which return responses.",
                "Which component handles a request and returns a response?", 2,
                [("A view", True), ("A migration", False), ("A static image", False)],
            ),
            (
                "Templates", "Templates render HTML and use tags and filters to work with context values.",
                "Which two features can a Django template use?", 1,
                [("Template tags", True), ("Template filters", True), ("Database migrations", False)],
            ),
        ]
        for position, example in enumerate(examples, start=1):
            title, content, prompt, points, choices = example
            lesson, _ = Lesson.objects.get_or_create(
                course=course, title=title, defaults={"content": content, "position": position}
            )
            question, _ = Question.objects.get_or_create(
                course=course, prompt=prompt, defaults={"lesson": lesson, "points": points}
            )
            for label, correct in choices:
                Choice.objects.get_or_create(
                    question=question, text=label, defaults={"is_correct": correct}
                )
        self.stdout.write(self.style.SUCCESS(f"Demo course ready at /courses/{course.pk}/"))
