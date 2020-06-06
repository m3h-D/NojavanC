from celery import app, shared_task, task

# # @shared_task
# # def hello():
# #     print("Hello there!") 


# @app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
# def add(self, x, y):
#     try:
#         something_raising()
#     except Exception as exc:
#         # overrides the default delay to retry after 1 minute
#         raise self.retry(exc=exc, countdown=60)



# @app.task(autoretry_for=(FailWhaleError,),
#           retry_kwargs={'max_retries': 5})
# def refresh_timeline(user):
#     return twitter.refresh_timeline(user)

# import sys
# import os

# print(sys.executable)
# print(os.getenv("ONE", "Not Found"))


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

@shared_task
def send_email():
    return print("OK lallalalallallalla")
    # try:
    #     message = render_to_string(kwargs.get("template"), {
    #         'sub': kwargs.get('sub'),
    #         'messages': [message for message in kwargs.get("messages")],
    #         'domain': kwargs.get("domain") if kwargs.get("domain") else None,
    #         'to': kwargs.get("to")[0],
    #     })
    #     subject, from_email = kwargs.get('sub'), 'support@100startups.ir'
    #     # logger.info(f"email{message}---{to_the}")
    #     text_content = strip_tags(message)
    #     msg = EmailMultiAlternatives(
    #         subject, text_content, from_email, [client for client in kwargs.get('to')] )
    #     msg.attach_alternative(message, 'text/html')
    #     msg.send()
    # except Exception as e:
    #     # logger.error(str(e))
    #     print(str(e))
    # return True