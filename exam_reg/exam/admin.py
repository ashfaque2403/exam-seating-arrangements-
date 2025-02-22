from django.contrib import admin
from .models import Student, ExamHall,Data,GereratingExam


admin.site.register(GereratingExam)
admin.site.register(Data)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):   
    pass

@admin.register(ExamHall)
class ExamHallAdmin(admin.ModelAdmin):
    pass
