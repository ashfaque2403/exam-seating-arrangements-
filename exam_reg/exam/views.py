from django.shortcuts import render,redirect
from .models import Student,ExamHall
# Create your views here.
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.contrib import messages
from itertools import groupby
from operator import itemgetter
from .models import ExamHall, Data, GereratingExam
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth import update_session_auth_hash



def save_data(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        rows = int(request.POST.get('rows'))
        columns = int(request.POST.get('columns'))
        hall_name = request.POST.get('hall_name')

        if hall_name:
            # Get or create the exam hall
            try:
                exam_hall = ExamHall.objects.get(name=hall_name)
            except ExamHall.DoesNotExist:
                exam_hall = ExamHall.objects.create(name=hall_name)
            except ExamHall.MultipleObjectsReturned:
                exam_hall = ExamHall.objects.filter(name=hall_name).first()
                
            # Check if there's already data associated with this exam hall
            if Data.objects.filter(exam_hall=exam_hall).exists():
                return JsonResponse({'error': 'Data already exists for this exam hall'})
            
            

            # Create data entries for each cell
            for i in range(rows):
                for j in range(columns):
                    subject_name = request.POST.get(f'row{i}col{j}')
                    roll_number = request.POST.get(f'row{i}col{j}_roll')
                    
                    if subject_name:
                        # Query student with the subject_name (department)
                        students = Student.objects.filter(department=subject_name) 
                        if students.exists():
                            # Choose the first student for simplicity, you might want to handle this differently
                            student = students.first()
                            Data.objects.create(
                                exam_hall=exam_hall,
                                subject_name=subject_name,
                                roll_number=roll_number,
                                row_number=i + 1,
                                column_number=j + 1,
                                student=student
                            )
                        else:
                            # Handle case when no student found for the given subject_name
                            return JsonResponse({'error': f'No student found for {subject_name}'})
                    else:
                        return JsonResponse({'error': 'Enter the Subject Name and Roll Number'})
            message = 'Are You Sure?'
            return JsonResponse({'message': message})
        else:
            # Alert message for missing exam hall name
            error_message = 'Exam hall name is required'
            return JsonResponse({'error': error_message})
    else:
        # Alert message for invalid request
        error_message = 'Invalid request'
        return JsonResponse({'error': error_message})





def subject_selector(request):
    halls = ExamHall.objects.all()
    student_list=Student.objects.all()
    return render(request, 'subject_selector.html', {'halls': halls , 'student_list': student_list})





def create_exam_hall(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')  # Assuming your form has a field with name 'name'

        if ExamHall.objects.filter(name=name).exists():
            messages.warning(request, 'Wrong Credentials')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            exam_hall = ExamHall.objects.create(name=name)
            messages.success(request, 'Created')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return redirect('create_exam_hall')  # Redirect to detail view of the created ExamHall
    else:
        # If it's a GET request, render a form to create the ExamHall
        return render(request, 'exam_hall_list.html')





def create_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        semester = request.POST.get('semester')
        department = request.POST.get('department')
        roll_number = request.POST.get('roll_number')

        if Student.objects.filter(roll_number=roll_number).exists():
            messages.warning(request, 'Student with this roll number already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            student = Student.objects.create(
                name=name,
                semester=semester,
                department=department,
                roll_number=roll_number
            )
            messages.success(request, 'Created Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to a page displaying list of students
    
    # Render the form template for GET requests as well
    return render(request, 'create_student.html')






def display_data(request):
    # Fetch all data from the Data model
    data_rows = Data.objects.all()

    # Organize data by exam hall and group by row number
    exam_halls_dict = {}
    for data in data_rows:
        if data.exam_hall:
            exam_hall_name = data.exam_hall.name
            if exam_hall_name not in exam_halls_dict:
                exam_halls_dict[exam_hall_name] = []

            exam_halls_dict[exam_hall_name].append({
                'row_number': data.row_number,
                'column_number': data.column_number,
                'subject_name': data.subject_name
            })

    # Group rows by row number within each exam hall
    for hall, rows in exam_halls_dict.items():
        rows.sort(key=itemgetter('row_number'))
        grouped_rows = []
        for row_number, group in groupby(rows, key=itemgetter('row_number')):
            grouped_rows.append(list(group))
        exam_halls_dict[hall] = grouped_rows

    return render(request, 'saved_data.html', {'exam_halls_dict': exam_halls_dict})




@login_required
def index(request):
    return render(request,'index.html')




def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_authenticated = authenticate(request, username=username, password=password)

        if not user_authenticated:
            messages.warning(request, 'Invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        print(f"Authenticated User: {user_authenticated}")

        login(request, user_authenticated)
        return redirect('/')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect(index)




def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email already exists
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            messages.warning(request, 'User with this email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Create a new CustomUser
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        # Redirect to the login page
        return redirect('login')

    # If the request method is not POST, render the registration page
    return render(request, 'register.html')





class GeneratePdf(View):
    def get(self, request, id, **kwargs):
        data_cols = Data.objects.all()
        data_rows = GereratingExam.objects.filter(id=id)
        exam = GereratingExam.objects.get(id=id)

        # Organize data by exam hall and group by row number
        exam_halls_dict = {}
        for data in data_rows:
            for hall in data.hall.all():
                exam_hall_name = hall.exam_hall.name
                if exam_hall_name not in exam_halls_dict:
                    exam_halls_dict[exam_hall_name] = []

                exam_halls_dict[exam_hall_name].append({
                    'row_number': hall.row_number,
                    'column_number': hall.column_number,
                    'subject_name': hall.subject_name,
                    'roll_number': hall.roll_number,
                })

        # Group rows by row number within each exam hall
        for hall, rows in exam_halls_dict.items():
            rows.sort(key=itemgetter('row_number'))
            grouped_rows = []
            for row_number, group in groupby(rows, key=itemgetter('row_number')):
                grouped_rows.append(list(group))
            exam_halls_dict[hall] = grouped_rows  # Retrieve the specific exam
            context = {'exam_halls_dict': exam_halls_dict,'semester': exam.semester}  # Pass exams data to the template
        pdf = render_to_pdf('examlist_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')




def ExamListed(request):
    exams = GereratingExam.objects.all()
    return render(request, 'examlist.html', {'exams': exams})




def delete(request,id):
    remove=GereratingExam.objects.filter(id=id)
    remove.delete()
    return redirect('exam_list_alls')




def Listing(request):
    examing = GereratingExam.objects.all().order_by('-created_at')
    current_time = timezone.now()

    for exam in examing:
        # Adds a boolean property 'is_new' to each exam instance
        exam.is_new = (current_time - exam.created_at) <= timedelta(days=2)
    return render(request, 'examlistall.html', {'examing': examing})



def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})




# from django.http import JsonResponse

def allot(request):
    if request.method == 'POST':
        exam_date = request.POST.get('exam_date')
        semester = request.POST.get('semester')
        exam_time = request.POST.get('exam_time')
        selected_halls = request.POST.getlist('hall_option')

        if GereratingExam.objects.filter(exam_date=exam_date).exists():
            return JsonResponse({'error': 'An exam is already scheduled for the selected date.'}, status=400)

        exam = GereratingExam.objects.create(exam_date=exam_date, exam_time=exam_time, semester=semester)
        for hall_name in selected_halls:
            hall_entries = Data.objects.filter(exam_hall__name=hall_name)
            exam.hall.add(*hall_entries)

        return JsonResponse({'success': 'Exams allotted successfully.'})

    distinct_exam_halls = ExamHall.objects.filter(data__isnull=False).distinct()
    return render(request, 'alot.html', {'distinct_exam_halls': distinct_exam_halls})





def allotted_exams(request):
    allotted_exams = GereratingExam.objects.all()
    semester_selection = GereratingExam.objects.all()
    return render(request, 'allotted_exams.html', {'allotted_exams': allotted_exams,'semester_selection':semester_selection})




def ExamList(request, id):
    # Fetch all data from the Data model
    data_cols = Data.objects.all()
    exam = GereratingExam.objects.get(id=id)
    data_rows = GereratingExam.objects.filter(id=id)
    data_full = GereratingExam.objects.all()

    # Organize data by exam hall and group by row number
    exam_halls_dict = {}
    for data in data_rows:
        for hall in data.hall.all():
            exam_hall_name = hall.exam_hall.name
            if exam_hall_name not in exam_halls_dict:
                exam_halls_dict[exam_hall_name] = []

            exam_halls_dict[exam_hall_name].append({
                'row_number': hall.row_number,
                'column_number': hall.column_number,
                'subject_name': hall.subject_name,
                'roll_number': hall.roll_number,
            })

    # Group rows by row number within each exam hall
    for hall, rows in exam_halls_dict.items():
        rows.sort(key=itemgetter('row_number'))
        grouped_rows = []
        for row_number, group in groupby(rows, key=itemgetter('row_number')):
            grouped_rows.append(list(group))
        exam_halls_dict[hall] = grouped_rows

    return render(request, 'examlist.html', {'exam_halls_dict': exam_halls_dict, 'exam_id': id,'semester': exam.semester })




def ChangePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the old password is correct
        if not authenticate(request, username=user.username, password=old_password):
            messages.error(request, 'Incorrect old password.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Update the session to prevent the user from being logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password successfully changed.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'changepassword.html')





def semester_view(request, semester_num):
    # Filter students by the selected semester
    student_list = Student.objects.filter(semester=str(semester_num))
    halls = ExamHall.objects.all()  # Assuming ExamHall model is defined elsewhere
    return render(request, 'subject_selector.html', {
        'halls': halls,
        'student_list': student_list,
        'selected_semester': semester_num
    })






def semester_selection(request):
    return render(request, 'semester_page.html')




def save_exam_data(request):
    # Check for POST request and AJAX header
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Process your data saving logic here
        try:
            # Example: create an exam object or similar
            # Exam.objects.create(...)
            return JsonResponse({'message': 'Data saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)