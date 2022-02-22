from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from portal_app.models import MCQ_Course, MCQ_Question, MCQ_Student, MCQ_Teacher, MCQ_Teaches, MCQ_Test

# Create your views here.
class Login(View):
    def get(self, request, template_name='login.html'):
        return render(request,template_name)

    def post(self,request,template_name='login.html'):
        message = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request,'Logged in successfully.')
                message = {}
                
                print(user.groups.all())
                if user.groups.filter(name='mcq_teacher').exists():
                    return redirect('TeacherDashboard')
                elif user.groups.filter(name='mcq_student').exists():
                    return redirect('StudentDashboard')
            else:
                messages.error(request,'Your account is disabled')
                return render(request, template_name)
        else:
            messages.error(request,'Invalid login details')
            return render(request, template_name)

def Logout(request):
    logout(request)
    return redirect('/')

class StudentDashboard(View):
    def get(self, request, template_name='studentdashboard.html'):
        message={}
        try:
            this_stud = MCQ_Student.objects.get(user=request.user)
            message['student']=this_stud
            active_tests = MCQ_Test.objects.filter(active=True)
            message['tests']=active_tests
        except:
            messages.error(request,'Login to access the page')
            redirect('Login')
        return render(request,template_name,message)

class TeacherDashboard(View):
    def get(self, request, template_name='teacherdashboard.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            active_tests = MCQ_Test.objects.all()
            message['tests']=active_tests
        except:
            messages.error(request,'Login to access the page')
            redirect('Login')
        return render(request,template_name,message)

class AddTest(View):
    def get(self, request, template_name='addtest.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            teaches = MCQ_Teaches.objects.filter(teacher=this_user,incharge=True)
            courses = MCQ_Course.objects.none()
            for i in teaches:
                courses |= MCQ_Course.objects.filter(course_id=i.course.course_id)
            message['courses']=courses
        except:
            messages.error(request,'Login to access the page')
            redirect('Login')
        return render(request,template_name,message)

    def post(self, request, template_name='addtest.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            test_id = request.POST.get('test_id')
            course = request.POST.get('course')
            course = MCQ_Course.objects.get(course_id=course)
            duration = request.POST.get('duration')
            active = request.POST.get('active')
            if active=="true":
                active=True
            else: 
                active=False
            try:
                new_test = MCQ_Test(test_id=test_id,course=course,duration=int(duration),active=active)
                new_test.save()
                messages.success(request,"Test added sucessfully")
                return redirect('TeacherDashboard')
            except:
                messages.error(request,'Something went wrong try again')
        except:
            messages.error(request,'Login to access the page')
            redirect('Login')
        return render(request,template_name,message)

class EditTest(View):
    def get(self, request, id, template_name='edittest.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            this_test = MCQ_Test.objects.get(test_id=id)
            course = MCQ_Course.objects.get(course_id=this_test.course.course_id)
            teaches = MCQ_Teaches.objects.get(teacher=this_user,course=course)
            message['test']=this_test
        except:
            messages.error(request,'Login to access the page')
            return redirect('Login')
        return render(request,template_name,message)

    def post(self, request, id, template_name='edittest.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            this_test = MCQ_Test.objects.get(test_id=id)
            course = MCQ_Course.objects.get(course_id=this_test.course.course_id)
            teaches = MCQ_Teaches.objects.get(teacher=this_user,course=course)
            message['test']=this_test
            duration = request.POST.get('duration')
            if duration:
                new_test = MCQ_Test.objects.filter(test_id=id).update(duration=int(duration))
            active = request.POST.get('active')
            if active=="true":
                active=True
                new_test = MCQ_Test.objects.filter(test_id=id).update(active=active)
            if active=="false": 
                active=False
                new_test = MCQ_Test.objects.filter(test_id=id).update(active=active)
            messages.success(request,"Test updated sucessfully")
            return redirect('TeacherDashboard')
        except:
            messages.error(request,'Login to access the page')
            return redirect('Login')
        return render(request,template_name,message)

class Questions(View):
    def get(self, request, id, template_name='questions.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            this_test = MCQ_Test.objects.get(test_id=id)
            course = MCQ_Course.objects.get(course_id=this_test.course.course_id)
            teaches = MCQ_Teaches.objects.get(teacher=this_user,course=course)
            message['test']=this_test
            questions = MCQ_Question.objects.filter(test=this_test)
            message["questions"]=questions
        except:
            messages.error(request,'Login to access the page')
            return redirect('Login')
        return render(request,template_name,message)

class AddQuestion(View):
    def get(self, request, id, template_name='addquestion.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            this_test = MCQ_Test.objects.get(test_id=id)
            course = MCQ_Course.objects.get(course_id=this_test.course.course_id)
            teaches = MCQ_Teaches.objects.get(teacher=this_user,course=course)
            message['test']=this_test
        except:
            messages.error(request,'Login to access the page')
            return redirect('Login')
        return render(request,template_name,message)

    def post(self, request, id, template_name='addquestion.html'):
        message={}
        try:
            this_user = MCQ_Teacher.objects.get(user=request.user)
            message['teacher']=this_user
            this_test = MCQ_Test.objects.get(test_id=id)
            course = MCQ_Course.objects.get(course_id=this_test.course.course_id)
            teaches = MCQ_Teaches.objects.get(teacher=this_user,course=course)
            message['test']=this_test

            try:
                question = request.POST.get("question")
                optionA = request.POST.get("optionA")
                optionB = request.POST.get("optionB")
                optionC = request.POST.get("optionC")
                optionD = request.POST.get("optionD")
                correct = request.POST.get("correct")
                marks = request.POST.get("marks")
                image = request.FILES.get("image")
                options = {"A":optionA,"B":optionB,"C":optionC,"D":optionD}
                print('got all')
                this_question = MCQ_Question(question=question,options=options,correct_option=correct,marks=int(marks),test=this_test)
                this_question.save()
                print("added que")

                if image:
                    print("taking img")
                    this_question = MCQ_Question.objects.filter(question=question)
                    print("got que")
                    this_question.update(image=image)
                    print("updates")
                    fss = FileSystemStorage()
                    file = fss.save(image.name,image)
                    print("saving")
                messages.success(request,'Question added')
                return redirect('Questions',id)
            except:
                messages.error(request,'Something went wrong, try again.')
                return render(request,template_name,message)

        except:
            messages.error(request,'Login to access the page')
            return redirect('Login')
        return render(request,template_name,message)