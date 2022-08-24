import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
  print("  Approved %r" % body)
  body = json.loads(body)
  print(body)
  presenter_name = body["name"]
  presenter_email = body["email"]
  title = body["title"]

  send_mail(
    'Your presentation has been accepted',
    f'Hello {presenter_name}. Your presentation {title} has been approved',
    'from@example.com',
    [f'{presenter_email}'],
    fail_silently=False,
  )


def process_rejections(ch, method, properties, body):
  print("  Rejected %r" % body)
  body = json.loads(body)
  print(body)
  presenter_name = body["name"]
  presenter_email = body["email"]
  title = body["title"]

  send_mail(
    'Your presentation has been Rejected',
    f'Hello {presenter_name}. Your presentation {title} has been rejected',
    'from@example.com',
    [f'{presenter_email}'],
    fail_silently=False,
  )



while True:
  try:
    parameters = pika.ConnectionParameters(host='rabbitmq')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="presentation_approvals")
    channel.queue_declare(queue="presentation_rejections")
    channel.basic_consume(
        queue="presentation_approvals",
        on_message_callback=process_approval,
        auto_ack=True,
    )
    channel.basic_consume(
        queue="presentation_rejections",
        on_message_callback=process_rejections,
        auto_ack=True,
    )
    channel.start_consuming()
  except AMQPConnectionError:
      print("Could not connect to RabbitMQ")
      time.sleep(2.0)