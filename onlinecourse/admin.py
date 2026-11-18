from django.contrib import admin

from .models import Choice, Course, Enrollment, Instructor, Lesson, Question, Submission


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ("course", "prompt", "points")
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("prompt", "course", "lesson", "points")
    list_filter = ("course",)
    search_fields = ("prompt",)
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position")
    list_filter = ("course",)
    inlines = [QuestionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "earned_points", "possible_points", "passed", "submitted_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register([Choice, Course, Enrollment, Instructor])
