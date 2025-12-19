from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import ContactForm, Olympiad, Subject


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contacts.html')


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactForm.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                status='not_processed'
            )
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact_form')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
    
    return render(request, 'contact_form.html')


def faq(request):
    return render(request, 'faq.html')


def rules(request):
    return render(request, 'rules.html')


def olympiads(request):
    """
    Отображает страницу со списком олимпиад.
    
    Получает активные олимпиады из базы данных, определяет их статус
    на основе текущей даты и передает в шаблон вместе со списком предметов.
    Автоматически деактивирует завершенные олимпиады.
    
    Returns:
        HttpResponse: Рендеринг шаблона olympiads.html с контекстом олимпиад и предметов.
    """
    now = timezone.now()
    Olympiad.objects.filter(is_active=True, end_date__lt=now).update(is_active=False)
    olympiads_list = Olympiad.objects.filter(is_active=True).prefetch_related('subjects__subject')
    
    olympiads_with_status = []
    for olympiad in olympiads_list:
        if olympiad.end_date < now:
            status = 'finished'
            status_display = 'Завершена'
        elif olympiad.start_date <= now <= olympiad.end_date:
            status = 'active'
            status_display = 'Активна'
        else:
            status = 'upcoming'
            status_display = 'Скоро'
        
        subjects_list = [olympiad_subject.subject for olympiad_subject in olympiad.subjects.filter(is_active=True)]
        subjects_names = [subject.name for subject in subjects_list]
        
        olympiads_with_status.append({
            'olympiad': olympiad,
            'status': status,
            'status_display': status_display,
            'subjects': subjects_list,
            'subjects_names': subjects_names,
        })
    
    all_subjects = Subject.objects.filter(is_active=True).order_by('name')
    
    context = {
        'olympiads': olympiads_with_status,
        'subjects': all_subjects,
    }
    
    return render(request, 'olympiads.html', context)

