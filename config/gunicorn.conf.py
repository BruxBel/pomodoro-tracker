from multiprocessing import cpu_count

workers = (2 * cpu_count()) + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "127.0.0.1:8000"
