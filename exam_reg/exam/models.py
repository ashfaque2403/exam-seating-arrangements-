from django.db import models
from django.utils import timezone
from datetime import timedelta


class ExamHall(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = [
        ('1', 'Semester 1'),('2', 'Semester 2'),('3', 'Semester 3'),('4', 'Semester 4'),('5', 'Semester 5'),('6', 'Semester 6')
    ]

    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    roll_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.roll_number} - {self.department}"

class Data(models.Model):
    exam_hall = models.ForeignKey(ExamHall, on_delete=models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, null=True, blank=True)  # New field for roll numbers
    row_number = models.IntegerField()
    column_number = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} - {self.row_number} - {self.column_number}"

class GereratingExam(models.Model):
    GENDER_CHOICES = [
        ('1', 'Semester 1'),('2', 'Semester 2'),('3', 'Semester 3'),('4', 'Semester 4'),('5', 'Semester 5'),('6', 'Semester 6')
    ]
    exam_date = models.DateField(auto_now=False, auto_now_add=False)
    exam_time = models.TimeField(auto_now=False, auto_now_add=False)
    semester = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True, blank=True)

    hall = models.ManyToManyField(Data)  # Assuming Data is another model you have defined
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.exam_date} - {self.exam_time}"

    def is_new(self):
    # This checks if the creation date is within the last 2 days.
        return (timezone.now() - self.created_at) <= timedelta(days=2)


    