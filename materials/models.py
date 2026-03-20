from django.core.validators import FileExtensionValidator
from django.db import models


class Course(models.Model):
    """Модель курса"""

    title_course = models.CharField(
        max_length=250,
        verbose_name="Наименование курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/",
        verbose_name="Превью курса",
        help_text="Загрузите изображение для превью курса",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите подробное описание курса"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
        help_text="Отметьте, если курс доступен для просмотра",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="courses",
        null=True,
        blank=True,
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_course


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится урок",
    )
    title_lesson = models.CharField(
        max_length=250,
        verbose_name="Наименование урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите подробное описание урока",
        blank=True,
    )
    preview = models.ImageField(
        upload_to="lessons/",
        verbose_name="Превью урока",
        help_text="Загрузите изображение для превью урока",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Вставьте ссылку на видео", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="lessons",
        null=True,
        blank=True,
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "title_lesson"]

    def __str__(self):
        return f"{self.course.title_course} - {self.title_lesson}"


class Subscription(models.Model):
    """Модель подписки на обновления курса"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]  # Чтобы не было дублей подписок

    def __str__(self):
        return f"{self.user.email} -> {self.course.title_course}"
