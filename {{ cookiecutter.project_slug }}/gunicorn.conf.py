import multiprocessing
import os

wsgi_app = "{{ cookiecutter.project_slug }}.wsgi:application"
bind_port = os.getenv("VIRTUAL_PORT", "8000")
bind = f"0.0.0.0:{bind_port}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_tmp_dir = "/dev/shm"
loglevel = "info"
timeout = 120
