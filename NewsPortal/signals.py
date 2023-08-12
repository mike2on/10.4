'''
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up
from .models import Post


def send_notifications(preview, pk, post_header, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'post_text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=Post.post_link.through)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_link.all()
        subscribers: list[str] = []
        for post_link in categories:
            subscribers += post_link.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.post_header, subscribers)


@receiver(user_signed_up)
def send_greetings(**kwargs):
    request = kwargs['request']
    user = kwargs['user']

    send_mail(
        subject='Добро пожаловать',
        message='',
        html_message=render_to_string(
            'welcome_email.html',
            context={
                'user': user,
            },
            request=None,
            using=None
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],

    )
    return user
'''
