import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


from users.models import User
from .models import Subscription

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_email(course_id, course_title):
    """Асинхронная отправка писем подписчикам курса"""

    # Получаем всех подписчиков курса
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related(
        "user"
    )

    if not subscriptions.exists():
        return f"Нет подписчиков у курса {course_title}"

    # Собираем email адреса подписчиков
    recipient_list = [sub.user.email for sub in subscriptions]

    # Тема письма
    subject = f"Обновление курса: {course_title}"

    # Текст письма
    message = f"""
    Здравствуйте!

    Курс "{course_title}" был обновлен.

    Зайдите на платформу, чтобы посмотреть новые материалы.

    С уважением,
    Команда образовательной платформы
    """

    # Отправляем письмо всем подписчикам
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return (
            f"Письма отправлены {len(recipient_list)} подписчикам курса {course_title}"
        )
    except Exception as e:
        return f"Ошибка отправки: {str(e)}"


@shared_task
def deactivate_users():
    """Блокировка пользователя"""

    # Получаем всех пользователей с вильтром по is_active
    user = User.objects.filter(is_active=True)

    for u in user:
        if timezone.now() - u.last_login > timedelta(days=30):
            u.is_active = False
            u.save()
            # Добавляем логирование
            logger.info(f"Пользователь {u.username} заблокирован.")
            # Отправляем уведомление администратору
            send_mail(
                "Блокировка пользователя",
                f"Пользователь {u.username} был заблокирован, поскольку не заходил на платформу более 30 дней",
                settings.DEFAULT_FROM_EMAIL,
                ["ksyu_student_2026@mail.ru"],
            )
