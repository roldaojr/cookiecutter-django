import multiprocessing
import os

wsgi_app = "{{ cookiecutter.project_slug }}.wsgi:application"
bind_port = os.getenv("VIRTUAL_PORT", "8000")
bind = f"0.0.0.0:{bind_port}"
worker_per_cpu = int(os.getenv("WORKER_PER_CPU", 2))
workers = os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * worker_per_cpu + 1)
worker_class = os.getenv("WORKER_CLASS", "sync")
worker_tmp_dir = "/dev/shm"
if "WORKER_THREADS" in os.environ:
    threads = os.environ.get("WORKER_THREADS", 4)
loglevel = "info"
timeout = int(os.getenv("WORKER_TIMEOUT", 120))
