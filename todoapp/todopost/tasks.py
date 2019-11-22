from celery import task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Post
@task
def signup_mail(user_pk = None):
    user = User.objects.filter(pk = user_pk).first()
    send_mail('Welcome Me',
    'This is automate message',
    'fhuseynov803@gmail.com',
    ['gowat79313@mailhub24.com'],
    fail_silently=False)
    return None

@task
def notification(source_id):
    m1 = Post.objects.filter(pk=source_id).first()
    send_mail('Hey {}'.format(m1.author.username),
    'There are 10 minutes for finishing of post',
    'fhuseynov803@gmail.com',
    ['fariba9661@tmailcloud.com'],
    fail_silently=False)
    return None
