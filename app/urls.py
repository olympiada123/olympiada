"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact-form/', views.contact_form, name='contact_form'),
    path('faq/', views.faq, name='faq'),
    path('rules/', views.rules, name='rules'),
    path('olympiads/', views.olympiads, name='olympiads'),
    path('olympiads/<int:olympiad_id>/', views.olympiad_detail, name='olympiad_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('olympiads/<int:olympiad_id>/register/', views.register_for_olympiad, name='register_for_olympiad'),
    path('olympiads/create/', views.create_olympiad, name='create_olympiad'),
    path('olympiads/<int:olympiad_id>/edit/', views.edit_olympiad, name='edit_olympiad'),
    path('olympiads/<int:olympiad_id>/subjects/<int:subject_id>/questions/', views.manage_questions, name='manage_questions'),
    path('olympiads/<int:olympiad_id>/subjects/<int:subject_id>/questions/create/', views.create_question, name='create_question'),
    path('olympiads/<int:olympiad_id>/subjects/<int:subject_id>/start/', views.start_exam, name='start_exam'),
    path('exam/<int:session_id>/', views.take_exam, name='take_exam'),
    path('exam/<int:session_id>/save/', views.save_answer, name='save_answer'),
    path('exam/<int:session_id>/submit/', views.submit_exam, name='submit_exam'),
    path('exam/<int:session_id>/results/', views.exam_results, name='exam_results'),
    path('olympiads/<int:olympiad_id>/download-participants/', views.download_olympiad_participants, name='download_olympiad_participants'),
]
