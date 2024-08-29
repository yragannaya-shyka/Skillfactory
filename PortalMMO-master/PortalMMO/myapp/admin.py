from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class AdvertisementAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())


    class Meta:
        model = Advertisement
        fields = '__all__'

class AdvertisementAdmin(admin.ModelAdmin):
    form = AdvertisementAdminForm

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Category)
admin.site.register(Responses)
