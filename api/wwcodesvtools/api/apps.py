from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    # def ready(self):
    #     # flush expired tokens from the outstanding and the blacklist.
    #     # execute for the local runserver and production wsgi deployment
    #     import sys
    #     if sys.argv[1] in ["runserver", "wwcodesvtools.wsgi:application"]:
    #         from django.core.management import call_command
    #         call_command("flushexpiredtokens")
