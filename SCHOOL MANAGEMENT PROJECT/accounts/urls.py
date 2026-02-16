from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [

    # 👇 ROOT URL FIL
    path('', lambda request: redirect('login'), name='home'),

    # ================= LOGIN =================
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ================= DASHBOARD =================
    path("superadmin-dashboard/",views.superadmin_dashboard,name="superadmin_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("principal-dashboard/", views.principal_dashboard, name="principal_dashboard"),
    path("teacher-dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    #path("clerk-dashboard/", views.clerk_dashboard, name="clerk_dashboard"),

    # ================= STUDENTS =================
    path('students/add/', views.add_student, name='add_student'),
    path("students/edit/<int:id>/", views.student_edit, name="student_edit"),
    path("students/delete/<int:id>/", views.student_delete, name="student_delete"),  # 👈 ADD THIS
    path("students/", views.student_list, name="student_list"),
    path("students/<int:std>/", views.student_list, name="student_list"),

    # ================= TEACHERS =================
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),

    # ================= LC =================
    path("leaving/", views.leaving_certificate, name="leaving_certificate"),
    path("leaving/print/<int:student_id>/", views.leaving_print, name="leaving_print"),
    # certificates urls
    path("bonafide/", views.bonafide_certificate, name="bonafide_certificate"),
    path("bonafide/print/<int:student_id>/", views.bonafide_print, name="bonafide_print"),


    # SUPER ADMIN
    path("superadmin-dashboard/",views.superadmin_dashboard,name="superadmin_dashboard"),

# 🔹 USER
path("superadmin/users/add/", views.add_user, name="add_user"),
path("superadmin/users/", views.user_list, name="user_list"),
path("superadmin/users/edit/<int:id>/", views.edit_user, name="edit_user"),
path("superadmin/users/delete/<int:id>/", views.delete_user, name="delete_user"),


# School
    path("superadmin/schools/", views.school_list, name="school_list"),
    path("superadmin/schools/add/", views.add_school, name="add_school"),
    path('superadmin/schools/delete/<int:pk>/', views.delete_school, name='delete_school'),

    path("superadmin/users/", views.user_list, name="user_list"),
    path("superadmin/users/add/", views.add_user, name="add_user"),

    #****************payment cashfree***************************
#     path('payment-page/<int:student_id>/<int:lc>/', views.payment_page, name='payment_page'),
#     path("create-payment/", views.create_payment, name="create_payment"),
]
