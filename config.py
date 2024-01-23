from dotenv import load_dotenv
import os

load_dotenv()

# Variables de entorno
PASSWORD = os.getenv('PASSWORD_EMAIL')
EMAIL = os.getenv('EMAIL')
