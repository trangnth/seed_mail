import os
from dotenv import load_dotenv

load_dotenv()


class SmtpConfig:
    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT")
    mode = os.getenv("SMTP_MODE")

    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    rcpt_to = os.getenv("RCPT_TO")
    payload = os.getenv("SMTP_PAYLOAD")
