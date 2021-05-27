import uuid
from src.libs.logger import logger
from imapclient import IMAPClient
from src.configuration.imapconfig import ImapConfig
from src.configuration.domain import DomainConfig


SEEN = b"\\Seen"
SENT_FROM_WEBMAIL = "$SENT_FROM_WEBMAIL"

DRAFT = b"\\Draft"
DRAFT_FROM_WEBMAIL = "$DRAFT_FROM_WEBMAIL"

SEARCH_CRITERIA_BY_MESSAGE_HEADER_ID = 'HEADER "Message-ID" "{}"'
BODY = 'BODY[]'
MESSAGE_ID = 'BODY[HEADER.FIELDS (MESSAGE-ID)]'
FLAGS = 'FLAGS'
INTERNALDATE = 'INTERNALDATE'

FIELDS = [
    BODY
]

def generate_message_id(suffix=f"@{DomainConfig.domain}"):
    if not isinstance(suffix, str):
        suffix = str(suffix)

    return "".join(["<", str(uuid.uuid4()) + suffix, ">"])


def new_message(client, folder="Drafts", flags=(DRAFT, DRAFT_FROM_WEBMAIL)):
    try:
        uniq_id = generate_message_id()
        body = f"Message-ID: {uniq_id}"
        client.select_folder(folder)
        client.append(folder, body, flags=flags)
        res = client.search(
            SEARCH_CRITERIA_BY_MESSAGE_HEADER_ID.format(uniq_id)
        )
        return res[0], uniq_id
    except Exception as e:
        logger.error("Could not create new message: %r", e)
        return False


def new_imap_client():
    """Connect to imap server.

    Return imapclient instance or None if any exception occurs

    """
    try:
        client = IMAPClient(ImapConfig.host, ImapConfig.port, ssl=False)
        client.starttls()
        return client
    except Exception as e:
        logger.error("Failed to connect to imap server")


def login(client):
    """Login client using username and password

    client is IMAPClient instance

    """
    try:
        client.login(ImapConfig.user, ImapConfig.password)
        return True
    except Exception as e:
        logger.error("Could not login")
        return False


def send_message(client, payload, folder_name=None):
    try:
        if not folder_name:
            folder_name = "Sent"
        uniq_id = generate_message_id()
        body = f"Message-ID: {uniq_id}"
        payload = body + "\n" + payload
        client.select_folder(folder_name)
        client.append(folder_name, payload, flags=(SEEN, SENT_FROM_WEBMAIL))
        return True
    except Exception as e:
        logger.error("Could not create new message: %r", e)
        return False


def delete(client, folder):
    try:
        client.select(folder)
        typ, data = client.search(None, 'ALL')
        for num in data[0].split():
            client.store(num, '+FLAGS', '\\Deleted')
        client.expunge()
    except Exception as e:
        logger.error("Could not delete message: %r", e)
        return False
