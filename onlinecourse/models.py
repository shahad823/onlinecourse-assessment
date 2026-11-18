from django.conf import settings
from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=180)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    content = models.TextField()
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["position", "pk"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_course_enrollment"),
        ]

    def __str__(self):
        return f"{self.user} – {self.course}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    prompt = models.CharField(max_length=300)
    points = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.CheckConstraint(condition=models.Q(points__gt=0), name="positive_question_points"),
        ]

    def __str__(self):
        return self.prompt


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions")
    choices = models.ManyToManyField(Choice, blank=True)
    earned_points = models.PositiveIntegerField(default=0)
    possible_points = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    results = models.JSONField(default=list, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment} · Attempt {self.pk}"
