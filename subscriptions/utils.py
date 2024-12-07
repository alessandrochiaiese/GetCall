from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_subscription_email(user, plan):
    subject = f"Abbonamento {plan.name} attivato con successo!"
    message = render_to_string('subscriptions/email_subscription_success.html', {
        'user': user,
        'plan': plan,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
