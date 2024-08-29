from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import Responses, Advertisement


def send_new_responses(responses_user, responses_text, responses_post):

    html_content = render_to_string(
        template_name='responses_email.html',
        context={
            'post_author': responses_post.author,
            'responses_user': responses_user,
            'text': responses_text,
            'link': f'{settings.SITE_URL}/detail/{responses_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новый отклик на ваше объявление!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[responses_post.author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(post_save, sender=Responses)
def about_notify_new_responses(sender, instance, **kwargs):
    user = instance.user
    text = instance.text
    post = instance.post

    send_new_responses(user, text, post)


def send_accept_responses(responses_user, responses_post):
    html_content = render_to_string(
        template_name='accept_responses_email.html',
        context={
            'responses_user': responses_user,
            'link': f'{settings.SITE_URL}/detail/{responses_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Ваш отклик приняли!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[responses_user.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#сигнал принятия отклика
@receiver(post_save, sender=Responses)
def about_notify_accept_responses(sender, instance, **kwargs):
    user = instance.user
    post = instance.post #получаю поле внешний ключ на модель постов
    if instance.status:
        send_accept_responses(user, post)

def send_notifications(preview, pk, headline, subscribers_list, author):
    for s in subscribers_list:
        sub_name = s.username
        if sub_name != author.username:
            sub_email = [s.email]
            html_content = render_to_string(
                'post_created_email.html',
                {
                    'headline': headline,
                    'text': preview,
                    'link': f'{settings.SITE_URL}/detail/{pk}',
                    'sub_name': sub_name

                }
            )

            msg = EmailMultiAlternatives(
                subject='Новое объявление!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=sub_email,
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@receiver(post_save, sender=Advertisement)
def notify_about_new_post(sender, instance, **kwargs):
        categories = instance.category
        author = instance.author
        subscribers_list = []

        subscribers = categories.subscribers.all()
        subscribers_list += [s for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.headline, subscribers_list, author)


