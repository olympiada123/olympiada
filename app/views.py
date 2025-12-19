from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from .models import ContactForm, Olympiad, Subject, CustomUser, StudentRegistration, OlympiadSubject, Question, Answer, ExamSession, StudentAnswer, Result


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
        
        registration_status = None
        if now < olympiad.registration_start:
            registration_status = 'not_started'
        elif olympiad.registration_start <= now <= olympiad.registration_end:
            registration_status = 'open'
        else:
            registration_status = 'closed'
        
        subjects_list = [olympiad_subject.subject for olympiad_subject in olympiad.subjects.filter(is_active=True)]
        subjects_names = [subject.name for subject in subjects_list]
        
        olympiads_with_status.append({
            'olympiad': olympiad,
            'status': status,
            'status_display': status_display,
            'registration_status': registration_status,
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
    
    olympiad_subjects = olympiad.subjects.filter(is_active=True).select_related('subject')
    subjects_list = [os.subject for os in olympiad_subjects]
    
    is_registered = False
    registration = None
    registered_subject_ids = []
    if request.user.is_authenticated:
        registration = StudentRegistration.objects.filter(
            student=request.user,
            olympiad=olympiad
        ).prefetch_related('subjects').first()
        is_registered = registration is not None
        if registration:
            registered_subject_ids = [s.id for s in registration.subjects.all()]
    
    can_register = False
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        can_register = (
            olympiad.registration_start <= now <= olympiad.registration_end and
            not is_registered and
            status != 'finished'
        )
    
    context = {
        'olympiad': olympiad,
        'status': status,
        'status_display': status_display,
        'subjects': subjects_list,
        'olympiad_subjects': olympiad_subjects,
        'is_registered': is_registered,
        'registration': registration,
        'can_register': can_register,
        'registered_subject_ids': registered_subject_ids,
    }
    
    return render(request, 'olympiad_detail.html', context)


@login_required
def register_for_olympiad(request, olympiad_id):
    """
    Обрабатывает регистрацию студента на олимпиаду.
    
    Args:
        request: HTTP запрос.
        olympiad_id: ID олимпиады для регистрации.
    
    Returns:
        HttpResponse: Редирект на страницу деталей олимпиады с сообщением.
    """
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    user = request.user
    
    if user.is_superuser or user.is_staff:
        messages.error(request, 'Администраторы и кураторы не могут регистрироваться на олимпиады.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    if not user.student_id:
        messages.error(request, 'Для регистрации на олимпиаду необходимо указать номер студенческого билета в настройках профиля.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    now = timezone.now()
    
    if now < olympiad.registration_start:
        messages.error(request, 'Регистрация на олимпиаду еще не открыта.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    if now > olympiad.registration_end:
        messages.error(request, 'Регистрация на олимпиаду уже закрыта.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    existing_registration = StudentRegistration.objects.filter(
        student=user,
        olympiad=olympiad
    ).first()
    
    if existing_registration:
        messages.info(request, 'Вы уже зарегистрированы на эту олимпиаду.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    subjects_list = [olympiad_subject.subject for olympiad_subject in olympiad.subjects.filter(is_active=True)]
    
    if not subjects_list:
        messages.error(request, 'На олимпиаде нет доступных предметов.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    try:
        registration = StudentRegistration.objects.create(
            student=user,
            olympiad=olympiad
        )
        
        if subjects_list:
            registration.subjects.set(subjects_list[:olympiad.max_subjects_per_student])
        
        messages.success(request, f'Вы успешно зарегистрированы на олимпиаду "{olympiad.name}".')
    except Exception as e:
        messages.error(request, f'Произошла ошибка при регистрации: {str(e)}')
    
    return redirect('olympiad_detail', olympiad_id=olympiad_id)


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
        if request.POST.get('action') == 'update_contact_form_status':
            form_id = request.POST.get('form_id')
            new_status = request.POST.get('status')
            
            if not form_id:
                messages.error(request, 'Ошибка: не указан ID формы.')
                status_filter = request.GET.get('status_filter', '')
                if status_filter:
                    from django.urls import reverse
                    from urllib.parse import urlencode
                    return redirect(f"{reverse('profile')}?{urlencode({'status_filter': status_filter})}")
                return redirect('profile')
            
            if not new_status:
                messages.error(request, 'Ошибка: не указан статус.')
                status_filter = request.GET.get('status_filter', '')
                if status_filter:
                    from django.urls import reverse
                    from urllib.parse import urlencode
                    return redirect(f"{reverse('profile')}?{urlencode({'status_filter': status_filter})}")
                return redirect('profile')
            
            try:
                contact_form = ContactForm.objects.get(id=form_id)
                contact_form.status = new_status
                contact_form.save()
                messages.success(request, 'Статус формы обратной связи успешно обновлен.')
            except ContactForm.DoesNotExist:
                messages.error(request, 'Форма обратной связи не найдена.')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении статуса: {str(e)}')
            
            status_filter = request.GET.get('status_filter', '')
            if status_filter:
                from django.urls import reverse
                from urllib.parse import urlencode
                return redirect(f"{reverse('profile')}?{urlencode({'status_filter': status_filter})}")
            return redirect('profile')
        
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
        
        search_query = request.GET.get('user_search', '')
        if search_query:
            from django.urls import reverse
            from urllib.parse import urlencode
            return redirect(f"{reverse('profile')}?{urlencode({'user_search': search_query})}")
        return redirect('profile')
    
    registrations = None
    all_users = None
    search_query = None
    contact_forms = None
    status_filter = None
    curator_olympiads = None
    
    if not user.is_superuser and not user.is_staff:
        registrations = StudentRegistration.objects.filter(student=user).select_related('olympiad').prefetch_related('subjects', 'olympiad__subjects__subject').order_by('-registered_at')
    
    if user.is_staff and not user.is_superuser:
        curator_search = request.GET.get('curator_search', '').strip()
        curator_status_filter = request.GET.get('curator_status_filter', 'all')
        
        curator_olympiads_query = Olympiad.objects.all()
        
        if curator_search:
            curator_olympiads_query = curator_olympiads_query.filter(
                models.Q(name__icontains=curator_search) |
                models.Q(description__icontains=curator_search)
            )
        
        if curator_status_filter == 'active':
            curator_olympiads_query = curator_olympiads_query.filter(is_active=True)
        elif curator_status_filter == 'inactive':
            curator_olympiads_query = curator_olympiads_query.filter(is_active=False)
        
        curator_olympiads = curator_olympiads_query.prefetch_related('subjects__subject').order_by('-is_active', '-created_at')
    
    if user.is_superuser:
        search_query = request.GET.get('user_search', '').strip()
        if search_query:
            all_users = CustomUser.objects.filter(
                models.Q(username__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query) |
                models.Q(email__icontains=search_query)
            ).order_by('last_name', 'first_name', 'username')
        else:
            all_users = CustomUser.objects.none()
        
        status_filter = request.GET.get('status_filter', '')
        contact_forms = ContactForm.objects.all().order_by('-created_at')
    
    curator_search = None
    curator_status_filter = None
    if user.is_staff and not user.is_superuser:
        curator_search = request.GET.get('curator_search', '').strip()
        curator_status_filter = request.GET.get('curator_status_filter', 'all')
    
    context = {
        'user': user,
        'role': role,
        'registrations': registrations,
        'all_users': all_users,
        'search_query': search_query,
        'contact_forms': contact_forms,
        'status_filter': status_filter,
        'curator_olympiads': curator_olympiads,
        'curator_search': curator_search,
        'curator_status_filter': curator_status_filter,
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


@login_required
def create_olympiad(request):
    """
    Создает новую олимпиаду.
    
    Args:
        request: HTTP запрос. Может содержать POST данные с данными олимпиады.
    
    Returns:
        HttpResponse: Рендеринг шаблона create_olympiad.html или редирект на профиль.
    """
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для создания олимпиад.')
        return redirect('profile')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        registration_start = request.POST.get('registration_start')
        registration_end = request.POST.get('registration_end')
        max_subjects_per_student = request.POST.get('max_subjects_per_student', 1)
        subject_ids = request.POST.getlist('subjects')
        
        if not all([name, start_date, end_date, registration_start, registration_end]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            all_subjects = Subject.objects.filter(is_active=True).order_by('name')
            return render(request, 'create_olympiad.html', {'subjects': all_subjects})
        
        try:
            from datetime import datetime
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            registration_start_obj = datetime.strptime(registration_start, '%Y-%m-%dT%H:%M')
            registration_end_obj = datetime.strptime(registration_end, '%Y-%m-%dT%H:%M')
            
            if registration_start_obj >= registration_end_obj:
                messages.error(request, 'Дата начала регистрации должна быть раньше даты окончания регистрации.')
                all_subjects = Subject.objects.filter(is_active=True).order_by('name')
                return render(request, 'create_olympiad.html', {'subjects': all_subjects})
            
            if start_date_obj >= end_date_obj:
                messages.error(request, 'Дата начала олимпиады должна быть раньше даты окончания.')
                all_subjects = Subject.objects.filter(is_active=True).order_by('name')
                return render(request, 'create_olympiad.html', {'subjects': all_subjects})
            
            if registration_end_obj > start_date_obj:
                messages.error(request, 'Регистрация должна завершиться до начала олимпиады.')
                all_subjects = Subject.objects.filter(is_active=True).order_by('name')
                return render(request, 'create_olympiad.html', {'subjects': all_subjects})
            
            olympiad = Olympiad.objects.create(
                name=name,
                description=description,
                start_date=start_date_obj,
                end_date=end_date_obj,
                registration_start=registration_start_obj,
                registration_end=registration_end_obj,
                max_subjects_per_student=int(max_subjects_per_student) if max_subjects_per_student else 1
            )
            
            if subject_ids:
                for subject_id in subject_ids:
                    try:
                        subject = Subject.objects.get(id=subject_id, is_active=True)
                        OlympiadSubject.objects.create(
                            olympiad=olympiad,
                            subject=subject
                        )
                    except Subject.DoesNotExist:
                        continue
            
            messages.success(request, f'Олимпиада "{olympiad.name}" успешно создана.')
            return redirect('profile')
        except ValueError as e:
            messages.error(request, f'Ошибка в формате даты: {str(e)}')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при создании олимпиады: {str(e)}')
    
    all_subjects = Subject.objects.filter(is_active=True).order_by('name')
    context = {
        'subjects': all_subjects,
    }
    return render(request, 'create_olympiad.html', context)


@login_required
def edit_olympiad(request, olympiad_id):
    """
    Редактирует существующую олимпиаду.
    
    Args:
        request: HTTP запрос. Может содержать POST данные с данными олимпиады.
        olympiad_id: ID олимпиады для редактирования.
    
    Returns:
        HttpResponse: Рендеринг шаблона edit_olympiad.html или редирект на профиль.
    """
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для редактирования олимпиад.')
        return redirect('profile')
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        registration_start = request.POST.get('registration_start')
        registration_end = request.POST.get('registration_end')
        max_subjects_per_student = request.POST.get('max_subjects_per_student', 1)
        subject_ids = request.POST.getlist('subjects')
        is_active = request.POST.get('is_active') == 'on'
        
        if not all([name, start_date, end_date, registration_start, registration_end]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            all_subjects = Subject.objects.filter(is_active=True).order_by('name')
            current_subjects = [os.subject.id for os in olympiad.subjects.filter(is_active=True)]
            return render(request, 'edit_olympiad.html', {
                'olympiad': olympiad,
                'subjects': all_subjects,
                'current_subjects': current_subjects
            })
        
        try:
            from datetime import datetime
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            registration_start_obj = datetime.strptime(registration_start, '%Y-%m-%dT%H:%M')
            registration_end_obj = datetime.strptime(registration_end, '%Y-%m-%dT%H:%M')
            
            if registration_start_obj >= registration_end_obj:
                messages.error(request, 'Дата начала регистрации должна быть раньше даты окончания регистрации.')
                all_subjects = Subject.objects.filter(is_active=True).order_by('name')
                current_subjects = [os.subject.id for os in olympiad.subjects.filter(is_active=True)]
                return render(request, 'edit_olympiad.html', {
                    'olympiad': olympiad,
                    'subjects': all_subjects,
                    'current_subjects': current_subjects
                })
            
            if start_date_obj >= end_date_obj:
                messages.error(request, 'Дата начала олимпиады должна быть раньше даты окончания.')
                all_subjects = Subject.objects.filter(is_active=True).order_by('name')
                current_subjects = [os.subject.id for os in olympiad.subjects.filter(is_active=True)]
                return render(request, 'edit_olympiad.html', {
                    'olympiad': olympiad,
                    'subjects': all_subjects,
                    'current_subjects': current_subjects
                })
            
            olympiad.name = name
            olympiad.description = description
            olympiad.start_date = start_date_obj
            olympiad.end_date = end_date_obj
            olympiad.registration_start = registration_start_obj
            olympiad.registration_end = registration_end_obj
            olympiad.max_subjects_per_student = int(max_subjects_per_student) if max_subjects_per_student else 1
            olympiad.is_active = is_active
            olympiad.save()
            
            olympiad.subjects.all().delete()
            if subject_ids:
                for subject_id in subject_ids:
                    try:
                        subject = Subject.objects.get(id=subject_id, is_active=True)
                        OlympiadSubject.objects.create(
                            olympiad=olympiad,
                            subject=subject
                        )
                    except Subject.DoesNotExist:
                        continue
            
            messages.success(request, f'Олимпиада "{olympiad.name}" успешно обновлена.')
            return redirect('profile')
        except ValueError as e:
            messages.error(request, f'Ошибка в формате даты: {str(e)}')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при обновлении олимпиады: {str(e)}')
    
    all_subjects = Subject.objects.filter(is_active=True).order_by('name')
    current_subjects = [os.subject.id for os in olympiad.subjects.filter(is_active=True)]
    olympiad_subjects = olympiad.subjects.filter(is_active=True).select_related('subject')
    
    context = {
        'olympiad': olympiad,
        'subjects': all_subjects,
        'current_subjects': current_subjects,
        'olympiad_subjects': olympiad_subjects,
    }
    return render(request, 'edit_olympiad.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manage_questions(request, olympiad_id, subject_id):
    """
    Управление вопросами для предмета олимпиады (для кураторов).
    
    Args:
        request: HTTP запрос.
        olympiad_id: ID олимпиады.
        subject_id: ID предмета.
    
    Returns:
        HttpResponse: Рендеринг шаблона manage_questions.html.
    """
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    subject = get_object_or_404(Subject, id=subject_id)
    olympiad_subject = get_object_or_404(OlympiadSubject, olympiad=olympiad, subject=subject)
    
    questions = Question.objects.filter(olympiad_subject=olympiad_subject, is_active=True).order_by('order')
    
    context = {
        'olympiad': olympiad,
        'subject': subject,
        'olympiad_subject': olympiad_subject,
        'questions': questions,
    }
    return render(request, 'manage_questions.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_question(request, olympiad_id, subject_id):
    """
    Создание нового вопроса для предмета олимпиады.
    
    Args:
        request: HTTP запрос. Может содержать POST данные с данными вопроса.
        olympiad_id: ID олимпиады.
        subject_id: ID предмета.
    
    Returns:
        HttpResponse: Рендеринг шаблона create_question.html или редирект.
    """
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    subject = get_object_or_404(Subject, id=subject_id)
    olympiad_subject = get_object_or_404(OlympiadSubject, olympiad=olympiad, subject=subject)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        description = request.POST.get('description', '')
        scoring_method = request.POST.get('scoring_method', 'weighted_sum')
        base_points = request.POST.get('base_points', 1.0)
        max_points = request.POST.get('max_points', 1.0)
        min_points = request.POST.get('min_points', 0.0)
        difficulty_level = request.POST.get('difficulty_level', 'intermediate')
        order = request.POST.get('order', 0)
        
        if not text:
            messages.error(request, 'Текст вопроса обязателен.')
            return redirect('create_question', olympiad_id=olympiad_id, subject_id=subject_id)
        
        question = Question.objects.create(
            olympiad_subject=olympiad_subject,
            text=text,
            description=description,
            scoring_method=scoring_method,
            base_points=base_points,
            max_points=max_points,
            min_points=min_points,
            difficulty_level=difficulty_level,
            order=order
        )
        
        answer_texts = request.POST.getlist('answer_text[]')
        answer_weights = request.POST.getlist('answer_weight[]')
        
        for i, answer_text in enumerate(answer_texts):
            if answer_text.strip():
                weight = float(answer_weights[i]) if i < len(answer_weights) and answer_weights[i] else 0.0
                Answer.objects.create(
                    question=question,
                    text=answer_text.strip(),
                    correctness_weight=weight,
                    order=i
                )
        
        messages.success(request, f'Вопрос успешно создан.')
        return redirect('manage_questions', olympiad_id=olympiad_id, subject_id=subject_id)
    
    context = {
        'olympiad': olympiad,
        'subject': subject,
        'olympiad_subject': olympiad_subject,
    }
    return render(request, 'create_question.html', context)


@login_required
def start_exam(request, olympiad_id, subject_id):
    """
    Начать прохождение теста по предмету олимпиады.
    
    Args:
        request: HTTP запрос.
        olympiad_id: ID олимпиады.
        subject_id: ID предмета.
    
    Returns:
        HttpResponse: Рендеринг страницы теста или редирект.
    """
    if request.user.is_superuser or request.user.is_staff:
        messages.error(request, 'Кураторы и администраторы не могут проходить тесты.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    subject = get_object_or_404(Subject, id=subject_id)
    olympiad_subject = get_object_or_404(OlympiadSubject, olympiad=olympiad, subject=subject)
    
    registration = StudentRegistration.objects.filter(
        student=request.user,
        olympiad=olympiad,
        subjects=subject
    ).first()
    
    if not registration:
        messages.error(request, 'Вы не зарегистрированы на этот предмет олимпиады.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    now = timezone.now()
    if olympiad.start_date > now or olympiad.end_date < now:
        messages.error(request, 'Олимпиада сейчас не проводится.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    existing_session = ExamSession.objects.filter(
        student=request.user,
        olympiad_subject=olympiad_subject,
        registration=registration
    ).order_by('-attempt_number').first()
    
    attempt_number = 1
    if existing_session:
        attempt_number = existing_session.attempt_number + 1
    
    exam_session = ExamSession.objects.create(
        student=request.user,
        olympiad_subject=olympiad_subject,
        registration=registration,
        attempt_number=attempt_number,
        status='in_progress',
        started_at=now
    )
    
    questions = Question.objects.filter(
        olympiad_subject=olympiad_subject,
        is_active=True
    ).order_by('order')
    
    if not questions.exists():
        messages.error(request, 'Для этого предмета еще не добавлены вопросы.')
        return redirect('olympiad_detail', olympiad_id=olympiad_id)
    
    question_order = [q.id for q in questions]
    max_score = sum(float(q.max_points) for q in questions)
    
    exam_session.question_order = question_order
    exam_session.max_score = max_score
    exam_session.save()
    
    exam_session.start_test()
    
    return redirect('take_exam', session_id=exam_session.id)


@login_required
def take_exam(request, session_id):
    """
    Страница прохождения теста.
    
    Args:
        request: HTTP запрос.
        session_id: ID сессии экзамена.
    
    Returns:
        HttpResponse: Рендеринг страницы теста.
    """
    exam_session = get_object_or_404(ExamSession, id=session_id)
    
    if exam_session.student != request.user:
        messages.error(request, 'У вас нет доступа к этой сессии.')
        return redirect('profile')
    
    if exam_session.status not in ['in_progress', 'paused']:
        messages.info(request, 'Эта сессия уже завершена.')
        return redirect('exam_results', session_id=session_id)
    
    if not exam_session.question_order:
        messages.error(request, 'Вопросы не найдены.')
        return redirect('olympiad_detail', olympiad_id=exam_session.olympiad_subject.olympiad.id)
    
    current_index = exam_session.current_question_index
    if current_index >= len(exam_session.question_order):
        return redirect('submit_exam', session_id=session_id)
    
    question_id = exam_session.question_order[current_index]
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question, is_active=True).order_by('order')
    
    existing_answer = StudentAnswer.objects.filter(
        exam_session=exam_session,
        question=question
    ).first()
    
    selected_answer_ids = []
    if existing_answer:
        selected_answer_ids = [a.id for a in existing_answer.selected_answers.all()]
    
    context = {
        'exam_session': exam_session,
        'question': question,
        'answers': answers,
        'selected_answer_ids': selected_answer_ids,
        'current_index': current_index + 1,
        'total_questions': len(exam_session.question_order),
    }
    return render(request, 'take_exam.html', context)


@login_required
def save_answer(request, session_id):
    """
    Сохранить ответ студента на вопрос.
    
    Args:
        request: HTTP запрос. Содержит POST данные с выбранными ответами.
        session_id: ID сессии экзамена.
    
    Returns:
        HttpResponse: Редирект на следующий вопрос или завершение теста.
    """
    exam_session = get_object_or_404(ExamSession, id=session_id)
    
    if exam_session.student != request.user:
        messages.error(request, 'У вас нет доступа к этой сессии.')
        return redirect('profile')
    
    if exam_session.status not in ['in_progress', 'paused']:
        messages.info(request, 'Эта сессия уже завершена.')
        return redirect('exam_results', session_id=session_id)
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_answer_ids = request.POST.getlist('answers')
        
        question = get_object_or_404(Question, id=question_id)
        
        student_answer, created = StudentAnswer.objects.get_or_create(
            exam_session=exam_session,
            question=question
        )
        
        student_answer.selected_answers.clear()
        if selected_answer_ids:
            selected_answers = Answer.objects.filter(id__in=selected_answer_ids)
            student_answer.selected_answers.set(selected_answers)
        
        student_answer.check_answer()
        
        action = request.POST.get('action', 'next')
        
        if action == 'next':
            exam_session.current_question_index += 1
            exam_session.questions_answered_count = StudentAnswer.objects.filter(exam_session=exam_session).count()
            exam_session.save()
            
            if exam_session.current_question_index >= len(exam_session.question_order):
                return redirect('submit_exam', session_id=session_id)
            else:
                return redirect('take_exam', session_id=session_id)
        elif action == 'previous':
            if exam_session.current_question_index > 0:
                exam_session.current_question_index -= 1
                exam_session.save()
            return redirect('take_exam', session_id=session_id)
        elif action == 'submit':
            return redirect('submit_exam', session_id=session_id)
    
    return redirect('take_exam', session_id=session_id)


@login_required
def submit_exam(request, session_id):
    """
    Завершить тест и рассчитать результаты.
    
    Args:
        request: HTTP запрос.
        session_id: ID сессии экзамена.
    
    Returns:
        HttpResponse: Редирект на страницу результатов.
    """
    exam_session = get_object_or_404(ExamSession, id=session_id)
    
    if exam_session.student != request.user:
        messages.error(request, 'У вас нет доступа к этой сессии.')
        return redirect('profile')
    
    if exam_session.status == 'completed':
        return redirect('exam_results', session_id=session_id)
    
    now = timezone.now()
    exam_session.status = 'completed'
    exam_session.completed_at = now
    exam_session.calculate_score()
    exam_session.save()
    
    registration = exam_session.registration
    olympiad = exam_session.olympiad_subject.olympiad
    
    result, created = Result.objects.get_or_create(
        student=request.user,
        olympiad=olympiad
    )
    
    all_sessions = ExamSession.objects.filter(
        student=request.user,
        olympiad_subject__olympiad=olympiad,
        status='completed'
    )
    
    total_score = sum(float(session.final_score) for session in all_sessions)
    max_possible = sum(float(session.max_score) for session in all_sessions)
    
    result.total_score = total_score
    result.max_possible_score = max_possible
    result.calculate_percentage()
    result.save()
    
    return redirect('exam_results', session_id=session_id)


@login_required
def exam_results(request, session_id):
    """
    Отобразить результаты прохождения теста.
    
    Args:
        request: HTTP запрос.
        session_id: ID сессии экзамена.
    
    Returns:
        HttpResponse: Рендеринг страницы результатов.
    """
    exam_session = get_object_or_404(ExamSession, id=session_id)
    
    if exam_session.student != request.user:
        messages.error(request, 'У вас нет доступа к этой сессии.')
        return redirect('profile')
    
    student_answers = StudentAnswer.objects.filter(exam_session=exam_session).select_related('question').prefetch_related('selected_answers')
    
    context = {
        'exam_session': exam_session,
        'student_answers': student_answers,
    }
    return render(request, 'exam_results.html', context)

