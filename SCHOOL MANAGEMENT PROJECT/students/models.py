from django.db import models
from accounts.models import School

class Student(models.Model):
    register_no = models.CharField(max_length=50)
    student_id = models.CharField(max_length=50)
    aadhaar = models.CharField(max_length=12)

    first_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)

    birth_place = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    dob = models.DateField()
    admission_date = models.DateField()
    leaving_date = models.DateField(null=True, blank=True)

    last_std = models.CharField(max_length=20, blank=True)
    last_school = models.CharField(max_length=200, blank=True)

    admission_std = models.CharField(max_length=20)
    remark = models.TextField(blank=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} ({self.school.name})"
