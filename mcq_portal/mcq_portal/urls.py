"""mcq_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from argparse import Namespace
from django.contrib import admin
from django.urls import path
from portal_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login.as_view(),name="Login"),
    path('logout/',views.Logout,name='Logout'),
    path('student-dashboard/',views.StudentDashboard.as_view(),name="StudentDashboard"),
    path('teacher-dashboard/',views.TeacherDashboard.as_view(),name="TeacherDashboard"),
    path('add-test/',views.AddTest.as_view(),name="AddTest"),
    path('edit-test/<str:id>',views.EditTest.as_view(),name="EditTest"),
    path('questions/<str:id>',views.Questions.as_view(),name="Questions"),
    path('add-question/<str:id>',views.AddQuestion.as_view(),name="AddQuestion"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)