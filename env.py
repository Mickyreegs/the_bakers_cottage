# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv
# loading variables from .env file
load_dotenv() 

os.environ.setdefault(
    "DATABASE_URL", os.getenv("DATABASE_URL"))

os.environ.setdefault(
    "SECRET_KEY", os.getenv("SECRET_KEY")
)

os.environ.setdefault(
    "MAPS_KEY", os.getenv("MAPS_KEY")
)

os.environ.setdefault(
    "MAP_ID", os.getenv("MAP_ID")
)

os.environ.setdefault(
    "EMAILJS_PUBLIC_KEY", os.getenv("EMAILJS_PUBLIC_KEY")
)