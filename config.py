from datetime import timedelta

class Config:
          SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/okuosigy_okuosi_gypsum_db'

     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://okuosigy_okuosigy:Musiimenta@localhost/okuosigy_okuosi_gypsum_db'
     


from dotenv import load_dotenv # <-- reads .env automatically
import os

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


