from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.cache import never_cache
from django.utils.dateparse import parse_date
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.urls import reverse
# from django.conf import settings

from datetime import datetime, timedelta

from students.models import Student
from .models import School
from .decorators import superadmin_required

# import requests
# import uuid
import json


# ✅ ONLY Custom User
User = get_user_model()


# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            role = user.role.upper()   # 🔥 MAIN FIX
            request.user.refresh_from_db()

            if role == "SUPER_ADMIN":
                return redirect("superadmin_dashboard")
            elif role == "ADMIN":
                return redirect("admin_dashboard")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ================= ROLE REDIRECT =================
def redirect_by_role(user):
    if user.role == "SUPER_ADMIN":
        return redirect("superadmin_dashboard")
    elif user.role == "ADMIN":
        return redirect("admin_dashboard")
    elif user.role == "TEACHER":
        return redirect("teacher_dashboard")
    elif user.role == "PRINCIPAL":
        return redirect("principal_dashboard")
    else:
        return redirect("login")


# ================= SUPER ADMIN DASHBOARD =================
@login_required
@superadmin_required
def superadmin_dashboard(request):

    total_schools = School.objects.count()

    # exclude logged-in superadmin
    total_users = User.objects.exclude(
        id=request.user.id
    ).exclude(role="SUPER_ADMIN").count()

    role_data = (
        User.objects.exclude(role="SUPER_ADMIN")
        .values("role")
        .annotate(count=Count("id"))
    )

    roles = [r["role"] for r in role_data]
    role_counts = [r["count"] for r in role_data]

    dates, user_counts = [], []
    for i in range(6, -1, -1):
        day = now().date() - timedelta(days=i)
        dates.append(day.strftime("%d %b"))
        user_counts.append(
            User.objects.filter(date_joined__date=day).count()
        )

    return render(request, "accounts/superadmin/dashboard.html", {
        "total_schools": total_schools,
        "total_users": total_users,
        "roles_json": json.dumps(roles),
        "role_counts_json": json.dumps(role_counts),
        "dates_json": json.dumps(dates),
        "user_counts_json": json.dumps(user_counts),
    })


# ================= DASHBOARD =================

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from students.models import Student
from accounts.models import Teacher   # Make sure Teacher model exists here
import json


@login_required
def admin_dashboard(request):

    students = Student.objects.filter(school=request.user.school)

    total_students = students.count()
    total_lc = students.filter(leaving_date__isnull=False).count()
    active_students = students.filter(leaving_date__isnull=True).count()

    total_teachers = Teacher.objects.filter(
        school=request.user.school
    ).count()

    context = {
        "total_students": total_students,
        "total_lc": total_lc,
        "total_teachers": total_teachers,
    }

    return render(request, "accounts/Admin/admin_dashboard.html", context)


@login_required
def teacher_dashboard(request):
    return render(request, "accounts/teacher_dashboard.html")


@login_required
def principal_dashboard(request):
    return render(request, "accounts/principal_dashboard.html")


# ================= USER MANAGEMENT =================
@login_required
@superadmin_required
def user_list(request):

    users = User.objects.exclude(role="SUPER_ADMIN")

    q = request.GET.get("q")
    if q:
        users = users.filter(username__icontains=q)

    role = request.GET.get("role")
    if role:
        users = users.filter(role=role)

    school_id = request.GET.get("school")
    if school_id:
        users = users.filter(school_id=school_id)

    schools = School.objects.all()

    return render(request, "accounts/superadmin/user_list.html", {
        "users": users,
        "schools": schools
    })


@login_required
@superadmin_required
def add_user(request):
    schools = School.objects.filter(is_active=True)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        school_id = request.POST.get("school")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                school_id=school_id if role != "SUPER_ADMIN" else None
            )

            # Django admin permissions
            if role == "SUPER_ADMIN":
                user.is_staff = True
                user.is_superuser = True
            elif role in ["ADMIN", "TEACHER", "PRINCIPAL"]:
                user.is_staff = True

            user.save()
            messages.success(request, "User created successfully")
            return redirect("user_list")

    return render(request, "accounts/superadmin/add_user.html", {
        "schools": schools
    })


@login_required
@superadmin_required
def edit_user(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        user.role = request.POST.get("role")
        user.school_id = request.POST.get("school") or None
        user.save()
        return redirect("user_list")

    return render(request, "accounts/superadmin/edit_user.html", {
        "user": user,
        "schools": School.objects.all()
    })


@login_required
@superadmin_required
def delete_user(request, id):
    user = User.objects.get(id=id)

    if user.role != "SUPER_ADMIN":
        user.delete()

    return redirect("user_list")


# ================= SCHOOL =================
@login_required
@superadmin_required
def school_list(request):
    query = request.GET.get('q')

    schools = School.objects.all().order_by('-id')

    if query:
        schools = schools.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(code__icontains=query)
        )

    return render(request, 'accounts/superadmin/school_list.html', {
        'schools': schools,
        'query': query
    })

@login_required
@superadmin_required
def add_school(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip().upper()
        address = request.POST.get("address", "").strip()

        if not name or not code:
            messages.error(request, "❌ All fields are required")
            return redirect("add_school")

        if School.objects.filter(code=code).exists():
            messages.error(
                request,
                f"❌ School code '{code}' already exists"
            )
            return redirect("add_school")

        School.objects.create(
            name=name,
            code=code,
            address=address,
            is_active=True
        )

        messages.success(request, "✅ School added successfully")
        return redirect("school_list")

    return render(request, "accounts/superadmin/add_school.html")

@login_required
@superadmin_required
def delete_school(request, pk):
    school = get_object_or_404(School, pk=pk)
    school.delete()
    messages.success(request, "✅ School deleted successfully")
    return redirect("school_list")


# ================= LOGOUT =================
@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect("login")

# ================= STUDENTS =================
# ================= ADD STUDENT ==============

def parse_date(date_str):
    if not date_str:
        return None
    try:
        # dd/mm/yyyy
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        # yyyy-mm-dd
        return datetime.strptime(date_str, "%Y-%m-%d").date()

@login_required
def add_student(request):

    if request.method == "POST":

        dob_raw = request.POST.get("dob")

        if not dob_raw:
            messages.error(request, "Date of Birth is required!")
            return redirect("add_student")

        Student.objects.create(
            register_no=request.POST.get("register_no"),
            student_id=request.POST.get("student_id"),
            aadhaar=request.POST.get("aadhaar"),

            first_name=request.POST.get("first_name"),
            father_name=request.POST.get("father_name"),
            mother_name=request.POST.get("mother_name"),
            surname=request.POST.get("surname"),

            religion=request.POST.get("religion"),
            caste=request.POST.get("caste"),

            birth_place=request.POST.get("birth_place"),
            taluka=request.POST.get("taluka"),
            district=request.POST.get("district"),

            dob=parse_date(dob_raw),  # ✅ safe now
            admission_date=parse_date(request.POST.get("admission_date")),
            leaving_date=parse_date(request.POST.get("leaving_date")),

            last_std=request.POST.get("last_std"),
            last_school=request.POST.get("last_school"),

            admission_std=request.POST.get("admission_std"),
            remark=request.POST.get("remark"),

            school=request.user.school,
        )

        messages.success(request, "Student added successfully")
        return redirect("student_list")

    return render(request, "accounts/Admin/add_student.html")


@never_cache
@login_required
def student_list(request):

    students = Student.objects.filter(
        school=request.user.school
    )

    std = request.GET.get("std")
    search = request.GET.get("q", "")

    if std and std != "all":
        students = students.filter(admission_std=std)

    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(surname__icontains=search) |
            Q(register_no__icontains=search)
        )

    return render(
        request,
        "accounts/Admin/student_list.html",
        {
            "students": students,
            "student_count": students.count(),
            "std": std,
            "search": search,
        }
    )

@login_required
def student_edit(request, id):
    student = get_object_or_404(
        Student,
        id=id,
        school=request.user.school
    )

    if request.method == "POST":
        student.register_no = request.POST.get("register_no")
        student.admission_std = request.POST.get("admission_std")
        student.last_school = request.POST.get("last_school")
        student.reason_of_leaving = request.POST.get("reason_of_leaving")
        student.remark = request.POST.get("remark")

        student.save()

        messages.success(request, "✅ Student updated successfully")

        return redirect("student_list")

    return render(
        request,
        "accounts/Admin/student_edit.html",
        {"student": student}
    )

# ================= STUDENT DELETE =================
@login_required
def student_delete(request, id):

    student = get_object_or_404(
        Student,
        id=id,
        school=request.user.school
    )

    std = student.admission_std
    student.delete()

    messages.success(request, "🗑 Student deleted successfully")

    return redirect(f"/students/?std={std}")

# ================= TEACHERS =================
@login_required
def add_teacher(request):
    return render(request, "accounts/Admin/add_teacher.html")


@login_required
def teacher_list(request):
    return render(request, "accounts/Admin/teacher_list.html")

# ================= CERTIFICATES =================

@login_required
def certificate_dashboard(request):
    return render(request, "accounts/certificates/dashboard.html")


@login_required
def bonafide_certificate(request):
    """
    STEP 1: Select Class
    STEP 2: Search Register No
    STEP 3: Show Student + Generate Bonafide
    """

    # std = request.GET.get("std")
    # grn = request.GET.get("grn")

    # students = Student.objects.none()
    # student = None

    # # STEP 1: Class selected
    # if std:
    #     students = Student.objects.filter(
    #         admission_std=std,
    #         school=request.user.school
    #     )

    # # STEP 2: GRN search
    # if std and grn:
    #     student = get_object_or_404(
    #         Student,
    #         register_no=grn,
    #         admission_std=std,
    #         school=request.user.school
    #     )

    return render(
        request,
        "accounts/certificates/bonafide_certificate.html",
        {
            # "students": students,
            # "student": student,
            # "std": std,
        }
    )


@login_required
def bonafide_print(request, student_id):
    """
    FINAL PRINT VIEW
    """

    # student = get_object_or_404(
    #     Student,
    #     id=student_id,
    #     school=request.user.school
    # )

    return render(
        request,
        "accounts/certificates/bonafide_print.html",
        {
            # "student": student,
            # "today": timezone.now().date()
        }
    )


@login_required
def leaving_certificate(request):
    """
    STEP 1: Select Class
    STEP 2: Search Register No
    STEP 3: Show student + Generate LC
    """

    std = request.GET.get("std")
    grn = request.GET.get("grn")

    students = Student.objects.none()
    student = None
    not_found = False   # 👈 FLAG

    if std:
        students = Student.objects.filter(
            admission_std=std,
            school=request.user.school
        )

    if std and grn:
        student = Student.objects.filter(
            register_no=grn,
            admission_std=std,
            school=request.user.school
        ).first()

        if not student:
                messages.error(request, "❌ Student not found")

    return render(
        request,
        "accounts/certificates/leaving_certificate.html",
        {
            "students": students,
            "student": student,
            "std": std,
            "not_found": not_found
        }
    )


@login_required
def leaving_print(request, student_id):
    """
    FINAL PRINT VIEW
    """
    student = get_object_or_404(
        Student,
        id=student_id,
        school=request.user.school
    )

    return render(
        request,
        "accounts/certificates/leaving_print.html",
        {
            "student": student,
            "today": timezone.now().date()
        }
    )

# def create_payment(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request"}, status=400)

#     try:
#         lc = int(request.POST.get("lc"))
#         student_id = int(request.POST.get("student_id"))
#     except (TypeError, ValueError):
#         return JsonResponse({"error": "Invalid data"}, status=400)

#     if lc <= 0:
#         return JsonResponse({"error": "LC must be greater than 0"}, status=400)

#     # 🔒 Server-side amount calculation (security)
#     amount = float(lc * 20)

#     # 🔑 Unique Order ID
#     order_id = f"LC_{student_id}_{uuid.uuid4().hex[:8]}"

#     # 🧠 Save in session for verification later
#     request.session["lc_count"] = lc
#     request.session["student_id"] = student_id
#     request.session["order_id"] = order_id

#     url = "https://sandbox.cashfree.com/pg/orders"

#     payload = {
#         "order_id": order_id,
#         "order_amount": amount,
#         "order_currency": "INR",
#         "customer_details": {
#             "customer_id": str(student_id),
#             "customer_email": "test@gmail.com",
#             "customer_phone": "9999999999"
#         },
#         "order_meta": {
#             "return_url": f"http://127.0.0.1:8000/payment-success/?order_id={order_id}"
#         }
#     }

#     headers = {
#         "x-client-id": settings.CASHFREE_APP_ID,
#         "x-client-secret": settings.CASHFREE_SECRET,
#         "x-api-version": "2022-09-01",
#         "Content-Type": "application/json"
#     }

#     res = requests.post(url, json=payload, headers=headers)

#     if res.status_code != 200:
#         return JsonResponse({"error": res.json()}, status=400)

#     data = res.json()

#     if "payment_session_id" in data:
#         return JsonResponse({
#             "payment_session_id": data["payment_session_id"]
#         })

#     return JsonResponse({"error": data}, status=400)

def leaving_print(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(request,
                "accounts/certificates/leaving_print.html",
                {"student": student})
