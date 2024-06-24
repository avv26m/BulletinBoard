from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, UserResponseList, ResponseCreate, ResponseDelete, ResponseAccept, ConfirmUser


urlpatterns = [
    path('', PostList.as_view(), name='post'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('responses/', UserResponseList.as_view(), name='responses'),
    path('<int:pk>/response/create', ResponseCreate.as_view(), name='response_create'),
    path('response/<int:pk>/accept', ResponseAccept.as_view(), name='response_accept'),
    path('response/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),

]