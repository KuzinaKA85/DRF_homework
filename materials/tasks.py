from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription


@shared_task
def send_course_update_email(course_id, course_title):
    """Асинхронная отправка писем подписчикам курса"""

    # Получаем всех подписчиков курса
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user')

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
        return f"Письма отправлены {len(recipient_list)} подписчикам курса {course_title}"
    except Exception as e:
        return f"Ошибка отправки: {str(e)}"