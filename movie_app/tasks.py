import base64
import os
import smtplib
import ssl

import unidecode
from celery import group, chord
from django.core.mail import send_mail
from django.core.management import call_command

from celery._state import get_current_app
from pathlib import Path
from dotenv import load_dotenv

from movie_app.models import Suggest
from movie_project.celery import app

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


@app.task()
def add(x, y):
    print(x + y)


@app.task()
def get_suggest():
    sugg = Suggest.objects.all()
    list_data = []
    if len(sugg) > 1:
        for data in sugg:
            list_data.append(call_command_task.s('download', '-s', data.suggest))
            data.delete()
        result = chord(group(list_data), emails.s()).delay()
    else:
        print('Hay menos de 2 datos')


@app.task()
def call_command_task(command, *args, **kwargs):
    return call_command(command, *args, **kwargs)


@app.task()
def emails(messages):
    all_messages = ''
    for message in messages:
        all_messages += message+'\n\n'
    send_mail(
        'Movie',
        all_messages,
        'chxmorro@gmail.com',
        ['chxmorro@gmail.com'],
    )
