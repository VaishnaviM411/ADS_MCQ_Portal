from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MCQ_Student)
admin.site.register(MCQ_Teacher)
admin.site.register(MCQ_Course)
admin.site.register(MCQ_Teaches)
admin.site.register(MCQ_Test)
admin.site.register(MCQ_Question)
admin.site.register(MCQ_TestReport)