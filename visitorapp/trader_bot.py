from time import sleep
from visitorapp.models import Bot


def trading():
    while Bot.objects.all().first().is_working:
        print("bot is running")
        sleep(1)
