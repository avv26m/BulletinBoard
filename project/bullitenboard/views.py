from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post, UserResponse

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2  # количество записей на странице

class UserResponseList(ListView):
    model = UserResponse
    ordering = '-response_time'
    template_name = 'response.html'
    context_object_name = 'response'
    paginate_by = 2

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_detail'
