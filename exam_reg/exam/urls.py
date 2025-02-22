from django.urls import path
from . import views
from .views import GeneratePdf
urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.LoginView,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),

    path('students/', views.student_list, name='student_list'),
    path('create_exam_hall/', views.create_exam_hall, name='create_exam_hall'),

    path('display-data/', views.display_data, name='display_data'),
    path('saved-files/',views.ExamListed,name='saved_files'),
    path('select/', views.subject_selector, name='subject_selector'),
    path('save-data/', views.save_data, name='save_data'),
    path('create_student/', views.create_student, name='create_student'),
    path('exam/<int:id>', views.ExamList, name='exam_list'),
    path('examing/', views.Listing, name='exam_list_alls'),
    path('changepassword/',views.ChangePassword,name='change-password'),
    path('remove/<int:id>',views.delete,name='delete_pdf'),
    # urls.py
    path('path/to/save/data/', views.save_exam_data, name='save_data'),
    path('exam_list_all/', views.allot, name='exam_list_all'),

    path('pdf/<int:id>',GeneratePdf.as_view(),name='pdf'),

    path('semester/<int:semester_num>/', views.semester_view, name='semester_view'),
    # path('semester/<int:semester_num>/', semester_view, name='semester_view'),
    path('semester/', views.semester_selection, name='semester_selection'),

    path('allotted_exams/', views.allotted_exams, name='allotted_exams'),

    
]
