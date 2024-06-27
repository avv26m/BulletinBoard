from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import UserResponse


@receiver(post_save, sender=UserResponse)
def my_handler(sender, instance, **kwargs):
    if instance.status:
        mail = instance.commentator.email
        send_mail(
            subject='Подтверждение отклика',
            message='Ваш отклик приняли)',
            from_email='Qdim2002@yandex.ru',
            recipient_list=[mail],
            fail_silently=False,
        )
    else:
        mail = instance.advertisement.author.email
        send_mail(
            subject='Подтверждение отклика',
            message='Подтвердите получение отклика',
            from_email='Qdim2002@yandex.ru',
            recipient_list=[mail],
            fail_silently=False,
        )