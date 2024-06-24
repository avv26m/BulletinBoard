from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm, UserResponseForm, AcceptResponseForm
from .models import Post, UserResponse, User
from .filters import PostFilter, ResponsesFilter
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

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = UserResponse.objects.filter(post__author__id=self.request.user.id)
        self.filterset = ResponsesFilter(self.request.GET, queryset, request=self.request.user.id)
        if not self.request.GET:
            return UserResponse.objects.none()
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['get'] = self.request.GET
        return context

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

    def form_valid(self, fors):
        post = fors.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(fors)

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
    success_url = reverse_lazy('post')
    permission_required = ('bullitenboard.create_response')

    def form_valid(self, fors):
        response = fors.save(commit=False)
        response.author = self.request.user
        response.post_id = self.kwargs['pk']
        response.save()
        return super().form_valid(fors)

class ResponseAccept(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = AcceptResponseForm
    model = UserResponse
    template_name = 'response_accept.html'
    success_url = reverse_lazy('responses')

class ResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = UserResponse
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses')

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalide_code.html')
        return redirect('account_login')