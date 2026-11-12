
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import StudentForm
from .models import Student, Job, JobApplication, Profile
from django.core.paginator import Paginator

# Home Page
def home(request):
    return render(request, "home.html")


# Student Form
def student_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            Student.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                course=form.cleaned_data["course"]
            )

            messages.success(request, "Student added successfully!")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "student_form.html", {"form": form})


# Student List
def student_list(request):
    students = Student.objects.all()

    return render(request, "student_list.html", {
        "students": students
    })


# Edit Student
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student.name = form.cleaned_data["name"]
            student.email = form.cleaned_data["email"]
            student.phone = form.cleaned_data["phone"]
            student.course = form.cleaned_data["course"]
            student.save()

            messages.success(request, "Student updated successfully!")
            return redirect("student_list")
    else:
        form = StudentForm(initial={
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "course": student.course
        })

    return render(request, "student_form.html", {"form": form})


# Delete Student
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()

    messages.success(request, "Student deleted successfully!")
    return redirect("student_list")


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            try:
                student = Student.objects.get(name__iexact=user.username)
                request.session["student_id"] = student.id
            except Student.DoesNotExist:
                pass

            return redirect("dashboard")

    return render(request, "login.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Job List with Search and Pagination
def job_list(request):
    query = request.GET.get("q", "").strip()

    jobs = Job.objects.order_by("-created_at")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query)
        )

    paginator = Paginator(jobs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "job_list.html", {
        "jobs": page_obj,
        "page_obj": page_obj,
        "query": query
    })



# Apply for Job
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)

    if "student_id" not in request.session:
        return redirect("login")

    student = Student.objects.get(
        id=request.session["student_id"]
    )

    already_applied = JobApplication.objects.filter(
        student=student,
        job=job
    ).exists()

    if already_applied:
        messages.warning(
            request,
            "You have already applied for this job."
        )
    else:
        JobApplication.objects.create(
            student=student,
            job=job
        )

        messages.success(
            request,
            "Application submitted successfully!"
        )

    return redirect("job_list")


# Dashboard
def dashboard(request):
    if "student_id" not in request.session:
        return redirect("login")

    total_jobs = Job.objects.count()
    student_id = request.session["student_id"]
    student = Student.objects.filter(id=student_id).first()

    total_applications = JobApplication.objects.filter(
        student_id=student_id
    ).count()

    return render(request, "dashboard.html", {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "student": student
    })


# Profile
def profile(request):
    if "student_id" not in request.session:
        return redirect("login")

    student = Student.objects.get(
        id=request.session["student_id"]
    )

    profile = Profile.objects.get(student=student)

    return render(request, "profile.html", {
        "student": student,
        "profile": profile
    })
# My Applications
def my_applications(request):
    if "student_id" not in request.session:
        return redirect("login")

    student = get_object_or_404(
        Student,
        id=request.session["student_id"]
    )

    applications = JobApplication.objects.filter(
        student=student
    ).select_related("job")

    return render(request, "my_applications.html", {
        "applications": applications
    })

# Edit Profile
def edit_profile(request):
    profile = Profile.objects.first()
    student = profile.student

    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.skills = request.POST.get("skills")
        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "student": student,
        "profile": profile
    })
def unapply_job(request, application_id):
    if request.method != "POST":
        return redirect("my_applications")

    student_id = request.session.get("student_id")

    if not student_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    application = JobApplication.objects.filter(
        id=application_id
    ).first()

    if application is None:
        messages.error(
            request,
            "Application not found. Please refresh the page."
        )
        return redirect("my_applications")

    if str(application.student_id) != str(student_id):
        messages.error(
            request,
            "You cannot cancel another student's application."
        )
        return redirect("my_applications")

    application.delete()

    messages.success(
        request,
        "Your application has been cancelled successfully."
    )

    return redirect("my_applications")
# Job Details
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    similar_jobs = Job.objects.filter(
        skills__icontains=job.skills
    ).exclude(id=job.id)[:3]

    return render(request, "student/job_detail.html", {
        "job": job,
        "similar_jobs": similar_jobs
    })