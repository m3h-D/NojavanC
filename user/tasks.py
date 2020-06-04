# # from celery import shared_task
# from celery import app

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

import sys
import os

print(sys.executable)
print(os.getenv("ONE", "Not Found"))