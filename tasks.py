from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True)
def send_welcome_email(self, user_email, username):
    subject = 'Welcome to Our Platform'
    message = f'Hi {username}, thank you for registering with us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)
    return f"Email sent to {user_email}"