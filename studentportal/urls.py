from django.contrib import admin
from django.urls import path
from student import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),

    path('student-form/', views.student_form, name='student_form'),
    path('student-list/', views.student_list, name='student_list'),

    path('student-edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student-delete/<int:id>/', views.student_delete, name='student_delete'),
    path('job-list/', views.job_list, name='job_list'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('profile/', views.profile, name='profile'),
    path("logout/", views.logout_view, name="logout"),
    path('apply-job/<int:id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("unapply/<int:application_id>/", views.unapply_job, name="unapply-job"),
    path('job-detail/<int:job_id>/', views.job_detail, name='job-detail'),
]