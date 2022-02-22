from django.db.models import OneToOneField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE

# Create your models here.
class MCQ_Student(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=CASCADE)

    def __str__(self):
        return self.user.username

class MCQ_Teacher(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=CASCADE)

    def __str__(self):
        return self.user.username

class MCQ_Course(models.Model):
    course_id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_id

class MCQ_Teaches(models.Model):
    teacher = models.ForeignKey(MCQ_Teacher,on_delete=CASCADE)
    course = models.ForeignKey(MCQ_Course,on_delete=CASCADE)
    incharge = models.BooleanField(default=False)

    def __str__(self):
        return self.teacher.user.username + " " + self.course.course_id

class MCQ_Test(models.Model):
    test_id = models.CharField(max_length=50,primary_key=True)
    course = models.ForeignKey(MCQ_Course,on_delete=SET_NULL,null=True)
    duration = models.IntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.test_id

class MCQ_Question(models.Model):
    question = models.TextField()
    options = models.JSONField()
    correct_option = models.CharField(max_length=1)
    test = models.ForeignKey(MCQ_Test,on_delete=SET_NULL,null=True)
    image = models.ImageField(blank=True)
    marks = models.IntegerField()

    def __str__(self):
        return self.question

class MCQ_TestReport(models.Model):
    student = models.ForeignKey(MCQ_Student,on_delete=CASCADE)
    question = models.ForeignKey(MCQ_Question,on_delete=CASCADE)
    answer = models.CharField(max_length=1)
    test = models.ForeignKey(MCQ_Test,on_delete=CASCADE)
    marks_obtained = models.IntegerField()

    def __str__(self):
        return self.student.user.username + " " + self.test.test_id