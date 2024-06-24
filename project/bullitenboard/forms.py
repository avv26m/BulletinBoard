import random
from string import hexdigits

from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.core.mail import send_mail

from .models import Post, UserResponse
from project import settings


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = ['title','category', 'text']
        labels = {'title':'Заголовок','category':'Категория', 'text':'Текст объявления'}



    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text',]
        labels = {'text': 'Содержание коментария'}


class AcceptResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text', 'status']
        labels = {'text': 'Содержание коментария'}

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user
