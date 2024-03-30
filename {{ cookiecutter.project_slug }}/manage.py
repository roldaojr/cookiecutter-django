#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


"""Run administrative tasks."""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings")
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc


def main():
    sys.argv[0] = "manage.py"
    execute_from_command_line(sys.argv)


def server():
    sys.argv[0] = "manage.py"
    sys.argv.insert(1, "runserver")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
