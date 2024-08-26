import os

from dotenv import load_dotenv
from uvicorn.workers import UvicornWorker


bind = "127.0.0.1:8000"
workers = 4
worker_class = UvicornWorker

environment = os.getenv("ENVIRONMENT")


env = os.path.join(os.getcwd(), f".{environment}.env")
if os.path.exists(env):
    load_dotenv(env)