import os
from dotenv import load_dotenv

load_dotenv()


class DomainConfig:
    domain = os.getenv("DOMAIN")
