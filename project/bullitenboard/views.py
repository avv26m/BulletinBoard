from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm, UserResponseForm
from .models import Post, UserResponse
from .filters import PostFilter
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

    def __str__(self):
        return

        # Переопределяем функцию получения списка товаров

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class UserResponseList(ListView):
    model = UserResponse
    ordering = '-response_time'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 2

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_detail'


# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, LoginRequiredMixin,  CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'
    permission_required = ('bullitenboard.add_post')

class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')
    permission_required = ('bullitenboard.change_post')

class ResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = UserResponseForm
    model = UserResponse
    template_name = 'response_create.html'
    success_url = reverse_lazy('posts')
    permission_required = ('bullitenboard.create_response')
