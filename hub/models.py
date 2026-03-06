from django.conf import settings
from django.db import models

class LearningUnit(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Semester(models.Model):
    SEM_CHOICES = [(1, "1st Semester"), (2, "2nd Semester")]
    unit = models.ForeignKey(LearningUnit, on_delete=models.CASCADE, related_name="semesters")
    number = models.IntegerField(choices=SEM_CHOICES)

    class Meta:
        unique_together = ("unit", "number")

    def __str__(self):
        return f"{self.unit.name} - {self.get_number_display()}"


class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Folder(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("subject", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.subject.title} / {self.name}"


class FileResource(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="files")
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="files")
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class Photo(models.Model):
    image = models.ImageField(upload_to="photos/")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.caption or f"Photo {self.pk}"


class Deadline(models.Model):
    title = models.CharField(max_length=150)
    due_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_at"]

    def __str__(self):
        return self.title


class Exam(models.Model):
    title = models.CharField(max_length=150)
    exam_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["exam_at"]

    def __str__(self):
        return self.title


class ClassEvent(models.Model):
    # 0=Mon ... 6=Sun
    day_of_week = models.IntegerField(choices=[
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ])
    title = models.CharField(max_length=150)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return self.title