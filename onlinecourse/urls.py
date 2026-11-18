from django.urls import path

from . import views

app_name = "onlinecourse"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("courses/<int:course_id>/submit/", views.submit, name="submit"),
    path(
        "courses/<int:course_id>/results/<int:submission_id>/",
        views.show_exam_result,
        name="show_exam_result",
    ),
]
