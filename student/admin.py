from django.contrib import admin
from .models import Student, Job, JobApplication, Profile

admin.site.register(Student)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Profile)