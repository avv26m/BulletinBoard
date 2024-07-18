from django.conf import settings
from django.core.mail import send_mail
from .models import UserResponse

def create_new_response(pk):
    response = UserResponse.objects.get(id=pk)
    send_mail(
        subject=f'Отклик на Ваше объявление!',
        message=f'Привет, {response.post.author}!\n'
                f'На ваше объявление "{response.respbulletins.title}" есть новый отклик.\n'
                f'"{response.author}" написал:\n "{response.text}"',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.post.author.email, ],
    )


def accept_response_message(pk):
    response = UserResponse.objects.get(id=pk)
    send_mail(
        subject=f'Ваш отклик принят!',
        message=f'Здравствуйте, {response.author}!\n'
                f'Ваш отклик на объявление "{response.post.title}" принят.\n'
                f'Посмотреть объявление целиком можно по ссылке:\n'
                f'http://127.0.0.1:8000/{response.post.id}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email,],
    )