import random
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import ModelForm
from myapp.models import Advertisement, Responses
from allauth.account.forms import SignupForm
from string import hexdigits
from django.core.mail import send_mail
from django.conf import settings


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
            recipient_list=[user.email]
        )
        return user


class PostForm(ModelForm):


    class Meta:
        model = Advertisement
        fields = [
            'headline',
            'text',
            'category',
        ]
        widgets = {
            'text': CKEditorUploadingWidget(),
        }


class ResponseForm(ModelForm):


    class Meta:
        model = Responses
        fields = [
            'text',
        ]
