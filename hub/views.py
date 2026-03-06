import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    LearningUnit, Semester, Subject, Folder, FileResource,
    Photo, Deadline, Exam, ClassEvent
)
from .forms import (
    SubjectForm, FolderForm, FileResourceForm, PhotoForm,
    DeadlineForm, ExamForm, ClassEventForm, AccountForm
)

User = get_user_model()

# Change these to your real links anytime
LOAD_URL = 'https://drive.google.com/drive/folders/1e4Rnbn-Pp2jnxZS2l-Qu5BF6Wj7KhpfC?usp=drive_link'
DRIVE_URL = 'https://drive.google.com/drive/folders/1wLeu00LImWVSyYMVBACizKn9baqs8fBP?usp=drive_link'


def landing(request):
    return render(request, "hub/landing.html")


@login_required
def learning_units(request):
    units = LearningUnit.objects.filter(name__in=["LU3", "LU4", "LU5", "LU6", "LU7"]).order_by("name")
    return render(request, "hub/learning_units.html", {"units": units})


@login_required
def unit_detail(request, unit_id):
    unit = get_object_or_404(LearningUnit, id=unit_id)
    return render(request, "hub/unit_detail.html", {"unit": unit})


@login_required
def semester_detail(request, unit_id, number):
    unit = get_object_or_404(LearningUnit, id=unit_id)
    semester = get_object_or_404(Semester, unit=unit, number=number)

    if request.method == "POST":
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            s = subject_form.save(commit=False)
            s.semester = semester
            s.created_by = request.user
            s.save()
            return redirect("semester_detail", unit_id=unit.id, number=number)
    else:
        subject_form = SubjectForm()

    subjects = semester.subjects.all()
    return render(request, "hub/semester_detail.html", {
        "unit": unit,
        "semester": semester,
        "subjects": subjects,
        "subject_form": subject_form
    })


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    folders = subject.folders.prefetch_related("files").all()
    loose_files = subject.files.filter(folder__isnull=True)

    folder_form = FolderForm()
    file_form = FileResourceForm()
    file_form.fields["folder"].queryset = folders

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_folder":
            folder_form = FolderForm(request.POST)
            if folder_form.is_valid():
                f = folder_form.save(commit=False)
                f.subject = subject
                f.created_by = request.user
                f.save()
                return redirect("subject_detail", subject_id=subject.id)

        if action == "upload_file":
            file_form = FileResourceForm(request.POST, request.FILES)
            file_form.fields["folder"].queryset = subject.folders.all()
            if file_form.is_valid():
                fr = file_form.save(commit=False)
                fr.subject = subject
                fr.uploaded_by = request.user
                fr.save()
                return redirect("subject_detail", subject_id=subject.id)

    return render(request, "hub/subject_detail.html", {
        "subject": subject,
        "folders": folders,
        "loose_files": loose_files,
        "folder_form": folder_form,
        "file_form": file_form,
    })


@login_required
def folder_rename(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == "POST":
        new_name = (request.POST.get("name") or "").strip()
        if new_name:
            folder.name = new_name
            folder.save()
    return redirect("subject_detail", subject_id=folder.subject_id)


@login_required
def folder_delete(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    subject_id = folder.subject_id
    if request.method == "POST":
        folder.delete()
    return redirect("subject_detail", subject_id=subject_id)


@login_required
def file_delete(request, file_id):
    f = get_object_or_404(FileResource, id=file_id)
    subject_id = f.subject_id
    if request.method == "POST":
        f.delete()
    return redirect("subject_detail", subject_id=subject_id)


@login_required
def photo_add(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.uploaded_by = request.user
            p.save()
    return redirect("home")


@login_required
def photo_delete(request, photo_id):
    p = get_object_or_404(Photo, id=photo_id)
    if request.method == "POST":
        p.delete()
    return redirect("home")


def _range_for_week(date_obj):
    start = date_obj - datetime.timedelta(days=date_obj.weekday())  # Monday
    end = start + datetime.timedelta(days=7)
    return start, end


@login_required
def home(request):
    today = timezone.localdate()
    tomorrow = today + datetime.timedelta(days=1)

    # Month calendar grid (highlight today)
    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_weeks = cal.monthdatescalendar(today.year, today.month)

    # Classes today/tomorrow
    classes_today = ClassEvent.objects.filter(day_of_week=today.weekday())
    classes_tomorrow = ClassEvent.objects.filter(day_of_week=tomorrow.weekday())

    # Deadlines/exams this & next week
    this_start, this_end = _range_for_week(today)
    next_start, next_end = this_end, this_end + datetime.timedelta(days=7)

    def aware_start(d):  # start of day
        return timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))

    def aware_end(d):  # start of day
        return timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))

    deadlines_this_week = Deadline.objects.filter(due_at__gte=aware_start(this_start), due_at__lt=aware_end(this_end))
    deadlines_next_week = Deadline.objects.filter(due_at__gte=aware_start(next_start), due_at__lt=aware_end(next_end))

    exams_this_week = Exam.objects.filter(exam_at__gte=aware_start(this_start), exam_at__lt=aware_end(this_end))
    exams_next_week = Exam.objects.filter(exam_at__gte=aware_start(next_start), exam_at__lt=aware_end(next_end))

    photos = Photo.objects.all()
    photo_form = PhotoForm()

    return render(request, "hub/home.html", {
        "today": today,
        "tomorrow": tomorrow.strftime("%a, %b %d"),
        "month_weeks": month_weeks,

        "classes_today": classes_today,
        "classes_tomorrow": classes_tomorrow,

        "deadlines_this_week": deadlines_this_week,
        "deadlines_next_week": deadlines_next_week,

        "exams_this_week": exams_this_week,
        "exams_next_week": exams_next_week,

        "photos": photos,
        "photo_form": photo_form,

        "load_url": LOAD_URL,
        "drive_url": DRIVE_URL,
    })


@login_required
def deadlines(request):
    deadline_form = DeadlineForm()
    exam_form = ExamForm()

    if request.method == "POST":
        kind = request.POST.get("kind")
        if kind == "deadline":
            deadline_form = DeadlineForm(request.POST)
            if deadline_form.is_valid():
                d = deadline_form.save(commit=False)
                d.created_by = request.user
                d.save()
                return redirect("deadlines")

        if kind == "exam":
            exam_form = ExamForm(request.POST)
            if exam_form.is_valid():
                e = exam_form.save(commit=False)
                e.created_by = request.user
                e.save()
                return redirect("deadlines")

    return render(request, "hub/deadlines.html", {
        "deadline_form": deadline_form,
        "exam_form": exam_form,
        "deadlines": Deadline.objects.all(),
        "exams": Exam.objects.all(),
    })


@login_required
def deadline_delete(request, deadline_id):
    d = get_object_or_404(Deadline, id=deadline_id)
    if request.method == "POST":
        d.delete()
    return redirect("deadlines")


@login_required
def exam_delete(request, exam_id):
    e = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        e.delete()
    return redirect("deadlines")


@login_required
def classes(request):
    form = ClassEventForm()
    if request.method == "POST":
        form = ClassEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("classes")

    today = timezone.localdate()
    return render(request, "hub/classes.html", {
        "form": form,
        "events": ClassEvent.objects.all(),
        "today_dow": today.weekday(),
    })


@login_required
def class_delete(request, event_id):
    ev = get_object_or_404(ClassEvent, id=event_id)
    if request.method == "POST":
        ev.delete()
    return redirect("classes")


@login_required
def account(request):
    form = AccountForm(instance=request.user)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account")

    return render(request, "hub/account.html", {"form": form})