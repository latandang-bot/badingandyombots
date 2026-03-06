from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home/", views.home, name="home"),

    # Academics hierarchy
    path("units/", views.learning_units, name="learning_units"),
    path("units/<int:unit_id>/", views.unit_detail, name="unit_detail"),
    path("units/<int:unit_id>/semester/<int:number>/", views.semester_detail, name="semester_detail"),
    path("subjects/<int:subject_id>/", views.subject_detail, name="subject_detail"),

    # Folder/file actions
    path("folders/<int:folder_id>/rename/", views.folder_rename, name="folder_rename"),
    path("folders/<int:folder_id>/delete/", views.folder_delete, name="folder_delete"),
    path("files/<int:file_id>/delete/", views.file_delete, name="file_delete"),

    # Photos
    path("photos/add/", views.photo_add, name="photo_add"),
    path("photos/<int:photo_id>/delete/", views.photo_delete, name="photo_delete"),

    # Schedule & deadlines
    path("classes/", views.classes, name="classes"),
    path("classes/<int:event_id>/delete/", views.class_delete, name="class_delete"),
    path("deadlines/", views.deadlines, name="deadlines"),
    path("deadlines/<int:deadline_id>/delete/", views.deadline_delete, name="deadline_delete"),
    path("exams/<int:exam_id>/delete/", views.exam_delete, name="exam_delete"),

    # Account
    path("account/", views.account, name="account"),
]