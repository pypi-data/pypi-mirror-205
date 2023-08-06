from django_tsp.conf import conf
from django.conf import settings


def say_hi():
    print("HELLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOO")

def greeting(name:str) -> None:
    print(name)

def print_company():
    print(conf.COMPANY_NAME)

def print_list():
    print(conf.NAME_LIST)

def say_ok():
    print(settings.get("RQ_NAME"))