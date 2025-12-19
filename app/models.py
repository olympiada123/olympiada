from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя для студентов
    """

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    student_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Студенческий билет",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Дата рождения"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()


class Subject(models.Model):
    """
    Модель предмета олимпиады
    """

    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название предмета"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Olympiad(models.Model):
    """
    Модель олимпиады
    """

    name = models.CharField(max_length=300, verbose_name="Название олимпиады")
    description = models.TextField(blank=True, verbose_name="Описание")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    registration_start = models.DateTimeField(verbose_name="Начало регистрации")
    registration_end = models.DateTimeField(verbose_name="Окончание регистрации")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    max_subjects_per_student = models.PositiveIntegerField(
        default=1, verbose_name="Максимум предметов на студента"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        """
        Автоматически деактивирует олимпиаду, если дата завершения прошла.
        """
        if self.end_date and self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OlympiadSubject(models.Model):
    """
    Связь олимпиады с предметами
    """

    olympiad = models.ForeignKey(
        Olympiad,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Олимпиада",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="olympiads",
        verbose_name="Предмет",
    )
    duration_minutes = models.PositiveIntegerField(
        default=60, verbose_name="Длительность (минуты)"
    )
    max_score = models.PositiveIntegerField(
        default=100, verbose_name="Максимальный балл"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Предмет олимпиады"
        verbose_name_plural = "Предметы олимпиады"
        unique_together = ["olympiad", "subject"]
        ordering = ["olympiad", "subject"]

    def __str__(self):
        return f"{self.olympiad.name} - {self.subject.name}"


class Question(models.Model):
    """
    Модель вопросов
    """

    SCORING_METHODS = [
        ("weighted_sum", "Взвешенная сумма ответов"),
        ("proportional", "Пропорциональное распределение"),
        ("threshold", "Пороговая система"),
        ("combinatorial", "Комбинаторная оценка"),
        ("adaptive", "Адаптивная оценка"),
    ]

    DIFFICULTY_LEVELS = [
        ("basic", "Базовый"),
        ("intermediate", "Средний"),
        ("advanced", "Продвинутый"),
        ("expert", "Экспертный"),
    ]

    olympiad_subject = models.ForeignKey(
        OlympiadSubject,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Предмет олимпиады",
    )
    text = models.TextField(verbose_name="Текст вопроса")
    description = models.TextField(blank=True, verbose_name="Дополнительное описание")
    scoring_method = models.CharField(
        max_length=20,
        choices=SCORING_METHODS,
        default="weighted_sum",
        verbose_name="Метод оценки",
    )
    base_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.0, verbose_name="Базовые баллы"
    )
    max_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.0, verbose_name="Максимальные баллы"
    )
    min_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Минимальные баллы"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default="intermediate",
        verbose_name="Уровень сложности",
    )
    estimated_time_seconds = models.PositiveIntegerField(
        default=60, verbose_name="Оценочное время (секунды)"
    )
    required_answers_count = models.PositiveIntegerField(
        default=1, verbose_name="Требуемое количество ответов"
    )
    allow_partial_selection = models.BooleanField(
        default=True, verbose_name="Разрешена частичная выборка"
    )
    shuffle_answers = models.BooleanField(
        default=False, verbose_name="Перемешивать варианты ответов"
    )
    penalty_for_wrong = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Штраф за неправильный ответ",
    )
    hint_available = models.BooleanField(
        default=False, verbose_name="Доступна подсказка"
    )
    hint_text = models.TextField(blank=True, verbose_name="Текст подсказки")
    hint_cost_points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Стоимость подсказки (баллы)",
    )
    depends_on_questions = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="dependent_questions",
        verbose_name="Зависит от вопросов",
    )
    answer_combination_rules = models.JSONField(
        default=dict, blank=True, verbose_name="Правила комбинаций ответов (JSON)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["olympiad_subject", "order"]
        indexes = [
            models.Index(fields=["olympiad_subject", "difficulty_level"]),
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return (
            f"{self.olympiad_subject} - Вопрос #{self.order} ({self.difficulty_level})"
        )

    def calculate_score(self, selected_answers):
        """
        Рассчитать баллы на основе выбранных ответов
        """
        if not selected_answers:
            return self.min_points

        total_weight = 0
        for answer in selected_answers:
            total_weight += answer.correctness_weight

        if self.scoring_method == "weighted_sum":
            score = self.base_points * total_weight
        elif self.scoring_method == "proportional":
            max_possible_weight = sum(a.correctness_weight for a in self.answers.all())
            if max_possible_weight > 0:
                score = self.max_points * (total_weight / max_possible_weight)
            else:
                score = 0
        elif self.scoring_method == "threshold":
            threshold = self.answer_combination_rules.get("threshold", 0.8)
            if total_weight >= threshold:
                score = self.max_points
            else:
                score = self.min_points
        elif self.scoring_method == "combinatorial":
            score = self._calculate_combinatorial_score(selected_answers)
        else:
            score = self.base_points * total_weight

        penalty = 0
        for answer in selected_answers:
            if answer.correctness_weight < 0:
                penalty += abs(answer.penalty_weight)

        final_score = max(self.min_points, min(self.max_points, score - penalty))
        return final_score

    def _calculate_combinatorial_score(self, selected_answers):
        """
        Комбинаторная оценка с учетом правил комбинаций
        """
        base_score = self.base_points
        combination_bonus = 0

        selected_ids = [str(a.id) for a in selected_answers]
        rules = self.answer_combination_rules

        if "combinations" in rules:
            for combo in rules["combinations"]:
                combo_answers = combo.get("answers", [])
                if set(selected_ids) == set(combo_answers):
                    combination_bonus = combo.get("bonus", 0)
                    break

        total_weight = sum(a.correctness_weight for a in selected_answers)
        score = base_score * total_weight + combination_bonus
        return score


class Answer(models.Model):
    """
    Модель варианта ответа с системой весов и зависимостей
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    text = models.TextField(verbose_name="Текст ответа")
    correctness_weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=0.0,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        verbose_name="Вес правильности (-1.0 до 1.0)",
    )
    partial_score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Частичные баллы"
    )
    penalty_weight = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.0, verbose_name="Вес штрафа"
    )
    explanation = models.TextField(blank=True, verbose_name="Объяснение ответа")
    difficulty_modifier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0,
        verbose_name="Модификатор сложности",
    )
    requires_other_answers = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="required_by_answers",
        verbose_name="Требует другие ответы",
    )
    conflicts_with_answers = models.ManyToManyField(
        "self",
        symmetrical=True,
        blank=True,
        verbose_name="Конфликтует с ответами",
    )
    priority = models.PositiveIntegerField(
        default=0, verbose_name="Приоритет отображения"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    metadata = models.JSONField(
        default=dict, blank=True, verbose_name="Метаданные (JSON)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ["question", "priority", "order"]
        indexes = [
            models.Index(fields=["question", "correctness_weight"]),
        ]

    def __str__(self):
        weight_str = f"{self.correctness_weight:.2f}"
        return f"{self.question} - Ответ #{self.order} (вес: {weight_str})"

    def is_fully_correct(self):
        """
        Проверить, является ли ответ полностью правильным
        """
        return self.correctness_weight >= 1.0

    def is_partially_correct(self):
        """
        Проверить, является ли ответ частично правильным
        """
        return 0.0 < self.correctness_weight < 1.0

    def is_incorrect(self):
        """
        Проверить, является ли ответ неправильным
        """
        return self.correctness_weight <= 0.0

    def get_effective_weight(self, context_answers=None):
        """
        Получить эффективный вес с учетом зависимостей
        """
        base_weight = self.correctness_weight

        if context_answers:
            required = self.requires_other_answers.all()
            if required:
                required_ids = {a.id for a in required}
                context_ids = {a.id for a in context_answers}
                if not required_ids.issubset(context_ids):
                    return 0.0

            conflicts = self.conflicts_with_answers.all()
            if conflicts:
                conflict_ids = {a.id for a in conflicts}
                context_ids = {a.id for a in context_answers}
                if conflict_ids.intersection(context_ids):
                    return -abs(self.penalty_weight)

        return base_weight * float(self.difficulty_modifier)


class StudentRegistration(models.Model):
    """
    Модель регистрации студента на олимпиаду
    """

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="Студент",
    )
    olympiad = models.ForeignKey(
        Olympiad,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="Олимпиада",
    )
    subjects = models.ManyToManyField(
        Subject, related_name="student_registrations", verbose_name="Предметы"
    )
    registered_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    class Meta:
        verbose_name = "Регистрация студента"
        verbose_name_plural = "Регистрации студентов"
        unique_together = ["student", "olympiad"]
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.student} - {self.olympiad}"


class ExamSession(models.Model):
    """
    Уникальная модель попытки прохождения теста с расширенным функционалом
    """

    STATUS_CHOICES = [
        ("not_started", "Не начата"),
        ("in_progress", "В процессе"),
        ("paused", "Приостановлена"),
        ("completed", "Завершена"),
        ("expired", "Истекла"),
        ("abandoned", "Прервана"),
        ("submitted", "Отправлена на проверку"),
    ]

    session_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, verbose_name="Токен сессии"
    )

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="exam_sessions",
        verbose_name="Студент",
    )
    registration = models.ForeignKey(
        StudentRegistration,
        on_delete=models.CASCADE,
        related_name="exam_sessions",
        verbose_name="Регистрация",
    )
    olympiad_subject = models.ForeignKey(
        OlympiadSubject,
        on_delete=models.CASCADE,
        related_name="exam_sessions",
        verbose_name="Предмет олимпиады",
    )

    attempt_number = models.PositiveIntegerField(
        default=1, verbose_name="Номер попытки"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started",
        verbose_name="Статус",
    )
    started_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Время начала"
    )
    completed_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Время завершения"
    )
    last_activity_at = models.DateTimeField(
        auto_now=True, verbose_name="Последняя активность"
    )

    is_paused = models.BooleanField(default=False, verbose_name="Приостановлена")
    paused_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Время приостановки"
    )
    pause_count = models.PositiveIntegerField(default=0, verbose_name="Количество пауз")
    total_pause_duration_seconds = models.PositiveIntegerField(
        default=0, verbose_name="Общая длительность пауз (секунды)"
    )

    current_question_index = models.PositiveIntegerField(
        default=0, verbose_name="Текущий вопрос (индекс)"
    )
    questions_answered_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество отвеченных вопросов"
    )

    question_order = models.JSONField(
        default=list, blank=True, verbose_name="Порядок вопросов (JSON)"
    )
    is_random_order = models.BooleanField(
        default=False, verbose_name="Случайный порядок вопросов"
    )

    question_timings = models.JSONField(
        default=dict, blank=True, verbose_name="Время на вопросы (JSON)"
    )
    time_spent_seconds = models.PositiveIntegerField(
        default=0, verbose_name="Потрачено времени (секунды)"
    )

    checkpoint_data = models.JSONField(
        default=dict, blank=True, verbose_name="Данные чекина (JSON)"
    )
    last_checkpoint_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Последний чекин"
    )

    score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Набранные баллы"
    )
    max_score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Максимальный балл"
    )
    penalty_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Штрафные баллы"
    )
    bonus_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Бонусные баллы"
    )
    final_score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Итоговый балл"
    )

    answer_changes_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество изменений ответов"
    )
    questions_skipped_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество пропущенных вопросов"
    )
    questions_reviewed_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотренных вопросов"
    )

    ip_address = models.GenericIPAddressField(
        blank=True, null=True, verbose_name="IP адрес"
    )
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    browser_fingerprint = models.CharField(
        max_length=255, blank=True, verbose_name="Отпечаток браузера"
    )

    allow_back_navigation = models.BooleanField(
        default=True, verbose_name="Разрешена навигация назад"
    )
    show_correct_answers = models.BooleanField(
        default=False, verbose_name="Показывать правильные ответы"
    )
    is_proctored = models.BooleanField(default=False, verbose_name="Прокторинг включен")

    suspicious_activities = models.JSONField(
        default=list, blank=True, verbose_name="Подозрительная активность (JSON)"
    )
    warning_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество предупреждений"
    )

    metadata = models.JSONField(
        default=dict, blank=True, verbose_name="Дополнительные метаданные (JSON)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Сессия экзамена"
        verbose_name_plural = "Сессии экзаменов"
        unique_together = [
            "student",
            "olympiad_subject",
            "registration",
            "attempt_number",
        ]
        ordering = ["-started_at", "-attempt_number"]
        indexes = [
            models.Index(fields=["session_token"]),
            models.Index(fields=["student", "olympiad_subject"]),
            models.Index(fields=["status", "started_at"]),
        ]

    def __str__(self):
        return (
            f"{self.student} - {self.olympiad_subject} (Попытка #{self.attempt_number})"
        )

    def start_test(self):
        """
        Начать тест
        """
        from django.utils import timezone

        if self.status == "not_started":
            self.status = "in_progress"
            self.started_at = timezone.now()
            self.last_activity_at = timezone.now()
            self.save()

    def pause_test(self):
        """
        Приостановить тест
        """
        from django.utils import timezone

        if self.status == "in_progress" and not self.is_paused:
            self.is_paused = True
            self.status = "paused"
            self.paused_at = timezone.now()
            self.pause_count += 1
            self.save()

    def resume_test(self):
        """
        Возобновить тест
        """
        from django.utils import timezone

        if self.is_paused and self.status == "paused":
            if self.paused_at:
                pause_duration = (timezone.now() - self.paused_at).total_seconds()
                self.total_pause_duration_seconds += int(pause_duration)
            self.is_paused = False
            self.status = "in_progress"
            self.paused_at = None
            self.last_activity_at = timezone.now()
            self.save()

    def save_checkpoint(self, checkpoint_data=None):
        """
        Сохранить чекпоинт (прогресс)
        """
        from django.utils import timezone

        if checkpoint_data:
            self.checkpoint_data = checkpoint_data
        else:
            self.checkpoint_data = {
                "current_question": self.current_question_index,
                "questions_answered": self.questions_answered_count,
                "time_spent": self.time_spent_seconds,
                "timestamp": timezone.now().isoformat(),
            }
        self.last_checkpoint_at = timezone.now()
        self.save()

    def record_question_time(self, question_id, seconds):
        """
        Записать время, потраченное на вопрос
        """
        if not self.question_timings:
            self.question_timings = {}
        self.question_timings[str(question_id)] = seconds
        self.time_spent_seconds += seconds
        self.save()

    def add_suspicious_activity(self, activity_type, description):
        """
        Добавить запись о подозрительной активности
        """
        from django.utils import timezone

        if not self.suspicious_activities:
            self.suspicious_activities = []

        self.suspicious_activities.append(
            {
                "type": activity_type,
                "description": description,
                "timestamp": timezone.now().isoformat(),
            }
        )
        self.warning_count += 1
        self.save()

    def calculate_score(self):
        """
        Метод для расчета набранных баллов с учетом штрафов и бонусов
        """
        student_answers = self.student_answers.all()
        total_score = 0

        for student_answer in student_answers:
            student_answer.check_answer()
            total_score += student_answer.points_earned

        self.score = total_score
        self.final_score = self.score + self.bonus_points - self.penalty_points

        if self.final_score < 0:
            self.final_score = 0

        self.save()
        return self.final_score

    def get_remaining_time_seconds(self):
        """
        Получить оставшееся время в секундах
        """
        if not self.started_at or not self.olympiad_subject.duration_minutes:
            return None

        from django.utils import timezone

        elapsed = (timezone.now() - self.started_at).total_seconds()
        elapsed -= self.total_pause_duration_seconds
        remaining = (self.olympiad_subject.duration_minutes * 60) - elapsed
        return max(0, int(remaining))

    def is_time_expired(self):
        """
        Проверить, истекло ли время
        """
        remaining = self.get_remaining_time_seconds()
        return remaining is not None and remaining <= 0


class StudentAnswer(models.Model):
    """
    Модель ответа студента на вопрос
    """

    exam_session = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name="student_answers",
        verbose_name="Сессия экзамена",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers",
        verbose_name="Вопрос",
    )
    selected_answers = models.ManyToManyField(
        Answer,
        related_name="student_selections",
        blank=True,
        verbose_name="Выбранные ответы",
    )
    text_answer = models.TextField(blank=True, verbose_name="Текстовый ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    points_earned = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Заработанные баллы"
    )
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Время ответа")

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студентов"
        unique_together = ["exam_session", "question"]
        ordering = ["question__order"]

    def __str__(self):
        return f"{self.exam_session.student} - {self.question}"

    def check_answer(self):
        """
        Метод для проверки правильности ответа
        """
        selected_answers = self.selected_answers.all()

        if not selected_answers:
            self.is_correct = False
            self.points_earned = 0
            self.save()
            return False

        calculated_score = self.question.calculate_score(selected_answers)
        self.points_earned = calculated_score

        total_weight = sum(
            answer.get_effective_weight(selected_answers) for answer in selected_answers
        )

        if total_weight >= 0.8:
            self.is_correct = True
        elif total_weight >= 0.3:
            self.is_correct = False
        else:
            self.is_correct = False

        self.save()
        return self.is_correct


class Result(models.Model):
    """
    Модель результатов олимпиады
    """

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Студент",
    )
    olympiad = models.ForeignKey(
        Olympiad,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Олимпиада",
    )
    total_score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Общий балл"
    )
    max_possible_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Максимально возможный балл",
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Процент выполнения (%)",
    )
    rank = models.PositiveIntegerField(blank=True, null=True, verbose_name="Место")
    completed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата завершения"
    )

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        unique_together = ["student", "olympiad"]
        ordering = ["-total_score", "completed_at"]

    def __str__(self):
        return f"{self.student} - {self.olympiad} - {self.total_score} баллов"

    def calculate_percentage(self):
        """
        Метод для расчета процента выполнения
        """
        if self.max_possible_score > 0:
            self.percentage = (self.total_score / self.max_possible_score) * 100
        else:
            self.percentage = 0
        self.save()
        return self.percentage


class ContactForm(models.Model):
    """
    Модель формы обратной связи
    """

    STATUS_CHOICES = [
        ("not_processed", "Не обработана"),
        ("in_progress", "В обработке"),
        ("reviewed", "Рассмотрена"),
    ]

    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_processed",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Форма обратной связи"
        verbose_name_plural = "Формы обратной связи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"