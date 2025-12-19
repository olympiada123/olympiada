from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import ContactForm, Olympiad, Subject, CustomUser, StudentRegistration


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


@login_required
def profile_view(request):
    """
    Отображает страницу личного кабинета пользователя.
    Для администраторов также отображает блок назначения ролей.
    
    Args:
        request: HTTP запрос. Может содержать POST данные для изменения ролей пользователей.
    
    Returns:
        HttpResponse: Рендеринг шаблона profile.html с данными пользователя.
    """
    user = request.user
    
    if user.is_superuser:
        role = 'Администратор'
    elif user.is_staff:
        role = 'Куратор'
    else:
        role = 'Студент'
    
    if request.method == 'POST' and user.is_superuser:
        target_user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        
        if target_user_id and new_role:
            try:
                target_user = CustomUser.objects.get(id=target_user_id)
                
                if target_user.id == user.id:
                    messages.error(request, 'Вы не можете изменить свою собственную роль.')
                else:
                    if new_role == 'admin':
                        target_user.is_superuser = True
                        target_user.is_staff = True
                    elif new_role == 'curator':
                        target_user.is_superuser = False
                        target_user.is_staff = True
                    elif new_role == 'student':
                        target_user.is_superuser = False
                        target_user.is_staff = False
                    
                    target_user.save()
                    messages.success(request, f'Роль пользователя {target_user.username} успешно изменена.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Пользователь не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при изменении роли: {str(e)}')
        
        return redirect('profile')
    
    registrations = StudentRegistration.objects.filter(student=user).select_related('olympiad').prefetch_related('subjects', 'olympiad__subjects__subject').order_by('-registered_at')
    
    all_users = None
    if user.is_superuser:
        all_users = CustomUser.objects.all().order_by('last_name', 'first_name', 'username')
    
    context = {
        'user': user,
        'role': role,
        'registrations': registrations,
        'all_users': all_users,
    }
    
    return render(request, 'profile.html', context)


@login_required
def settings_view(request):
    """
    Отображает страницу настроек пользователя и обрабатывает изменения.
    
    Args:
        request: HTTP запрос. Может содержать POST данные для обновления профиля.
    
    Returns:
        HttpResponse: Рендеринг шаблона settings.html или редирект на страницу настроек.
    """
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            student_id = request.POST.get('student_id', '').strip()
            
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if student_id:
                if CustomUser.objects.filter(student_id=student_id).exclude(id=user.id).exists():
                    messages.error(request, 'Студенческий билет с таким номером уже используется.')
                else:
                    user.student_id = student_id
            else:
                user.student_id = None
            
            user.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('settings')
        
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if not old_password or not new_password1 or not new_password2:
                messages.error(request, 'Пожалуйста, заполните все поля.')
                return redirect('settings')
            
            if not user.check_password(old_password):
                messages.error(request, 'Неверный текущий пароль.')
                return redirect('settings')
            
            if new_password1 != new_password2:
                messages.error(request, 'Новые пароли не совпадают.')
                return redirect('settings')
            
            try:
                validate_password(new_password1, user)
            except ValidationError as e:
                messages.error(request, '; '.join(e.messages))
                return redirect('settings')
            
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('settings')
    
    context = {
        'user': user,
    }
    
    return render(request, 'settings.html', context)

