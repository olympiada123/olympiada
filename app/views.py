from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ContactForm, Olympiad, Subject, CustomUser


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
    
    Получает активные или неактивные олимпиады из базы данных в зависимости от параметра show_past,
    определяет их статус на основе текущей даты и передает в шаблон вместе со списком предметов.
    Автоматически деактивирует завершенные олимпиады.
    
    Args:
        request: HTTP запрос. Может содержать GET параметр 'show_past' для отображения прошлых олимпиад.
    
    Returns:
        HttpResponse: Рендеринг шаблона olympiads.html с контекстом олимпиад и предметов.
    """
    now = timezone.now()
    show_past = request.GET.get('show_past', 'false').lower() == 'true'
    
    Olympiad.objects.filter(is_active=True, end_date__lt=now).update(is_active=False)
    
    if show_past:
        olympiads_list = Olympiad.objects.filter(is_active=False).prefetch_related('subjects__subject').order_by('-end_date')
    else:
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
        'show_past': show_past,
    }
    
    return render(request, 'olympiads.html', context)


def olympiad_detail(request, olympiad_id):
    """
    Отображает детальную информацию об олимпиаде.
    
    Args:
        request: HTTP запрос.
        olympiad_id: ID олимпиады для отображения.
    
    Returns:
        HttpResponse: Рендеринг шаблона olympiad_detail.html с контекстом олимпиады.
    """
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    now = timezone.now()
    
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
    
    context = {
        'olympiad': olympiad,
        'status': status,
        'status_display': status_display,
        'subjects': subjects_list,
    }
    
    return render(request, 'olympiad_detail.html', context)


def login_view(request):
    """
    Обрабатывает вход пользователя в систему.
    
    Args:
        request: HTTP запрос. Может содержать POST данные с username и password.
    
    Returns:
        HttpResponse: Рендеринг шаблона login.html или редирект на главную страницу.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'login.html')


def register_view(request):
    """
    Обрабатывает регистрацию нового пользователя.
    
    Args:
        request: HTTP запрос. Может содержать POST данные с данными пользователя.
    
    Returns:
        HttpResponse: Рендеринг шаблона register.html или редирект на главную страницу.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        agree_terms = request.POST.get('agree_terms')
        
        if not agree_terms:
            messages.error(request, 'Необходимо согласиться с правилами и условиями использования.')
            return render(request, 'register.html')
        
        if not all([username, email, first_name, last_name, password1, password2]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return render(request, 'register.html')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Пароль должен содержать минимум 8 символов.')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'register.html')
        
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.get_full_name() or user.username}!')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {str(e)}')
    
    return render(request, 'register.html')


@login_required
def logout_view(request):
    """
    Обрабатывает выход пользователя из системы.
    
    Args:
        request: HTTP запрос.
    
    Returns:
        HttpResponse: Редирект на главную страницу.
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')

