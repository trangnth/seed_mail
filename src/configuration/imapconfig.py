import os
from dotenv import load_dotenv

load_dotenv()


class ImapConfig:
    host = os.getenv("IMAP_HOST")
    port = os.getenv("IMAP_PORT")

    user = os.getenv("IMAP_USER")
    password = os.getenv("IMAP_PASSWORD")

    payload = os.getenv("SMTP_PAYLOAD")
