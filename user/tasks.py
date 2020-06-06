from celery import app, shared_task, task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email(**kwargs):
    try:
        message = render_to_string(kwargs.get("template"), {
            'sub': kwargs.get('sub'),
            'messages': [message for message in kwargs.get("messages")],
            'domain': kwargs.get("domain") if kwargs.get("domain") else None,
            'to': kwargs.get("to")[0],
        })
        subject, from_email = kwargs.get('sub'), 'support@100startups.ir'
        logger.success(f"email{message}---{kwargs.get('to')}")
        text_content = strip_tags(message)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [client for client in kwargs.get('to')] )
        msg.attach_alternative(message, 'text/html')
        msg.send()
    except Exception as e:
        logger.error(str(e))
    return True