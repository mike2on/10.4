import datetime
from celery import shared_task
from django.conf import settings
from .models import Category, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_link.all()
    title = post.post_header
    subscribers: list[str] = []
    for post_link in categories:
        subscribers += post_link.subscribers.all()

    html_content = render_to_string(
        'post_created_email.html',
        {
            'post_text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_notifications_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time_in__gte=last_week)
    categories = set(posts.values_list('post_link__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()
