from django import forms
from django.contrib.auth import get_user_model

from .models import Subject, Folder, FileResource, Photo, Deadline, Exam, ClassEvent

User = get_user_model()

def classy(widget):
    widget.attrs["class"] = (widget.attrs.get("class", "") + " form-control").strip()
    return widget

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["title"]
        widgets = {"title": classy(forms.TextInput(attrs={"placeholder": "e.g. Anatomy"}))}

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name"]
        widgets = {"name": classy(forms.TextInput(attrs={"placeholder": "e.g. Transes"}))}

class FileResourceForm(forms.ModelForm):
    class Meta:
        model = FileResource
        fields = ["folder", "title", "file"]
        widgets = {
            "folder": classy(forms.Select()),
            "title": classy(forms.TextInput(attrs={"placeholder": "File title"})),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "caption": classy(forms.TextInput(attrs={"placeholder": "optional caption"})),
        }

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ["title", "due_at", "notes"]
        widgets = {
            "title": classy(forms.TextInput(attrs={"placeholder": "Deadline title"})),
            "due_at": classy(forms.DateTimeInput(attrs={"type": "datetime-local"})),
            "notes": classy(forms.Textarea(attrs={"rows": 2, "placeholder": "optional notes"})),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["title", "exam_at", "notes"]
        widgets = {
            "title": classy(forms.TextInput(attrs={"placeholder": "Exam title"})),
            "exam_at": classy(forms.DateTimeInput(attrs={"type": "datetime-local"})),
            "notes": classy(forms.Textarea(attrs={"rows": 2, "placeholder": "optional notes"})),
        }

class ClassEventForm(forms.ModelForm):
    class Meta:
        model = ClassEvent
        fields = ["day_of_week", "title", "start_time", "end_time", "location"]
        widgets = {
            "day_of_week": classy(forms.Select()),
            "title": classy(forms.TextInput(attrs={"placeholder": "e.g. Lecture"})),
            "start_time": classy(forms.TimeInput(attrs={"type": "time"})),
            "end_time": classy(forms.TimeInput(attrs={"type": "time"})),
            "location": classy(forms.TextInput(attrs={"placeholder": "optional"})),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": classy(forms.TextInput()),
            "last_name": classy(forms.TextInput()),
            "email": classy(forms.EmailInput()),
        }