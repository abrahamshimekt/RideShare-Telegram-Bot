import os
from dotenv import load_dotenv

load_dotenv('.env')

# my token 
token = os.getenv('API_TOKEN')