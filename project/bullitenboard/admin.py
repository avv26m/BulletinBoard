from django.contrib import admin
from django import forms

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm



admin.site.register(Post, PostAdmin)
admin.site.register(UserResponse)
admin.site.register(User)