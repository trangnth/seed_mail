import uuid
import smtplib
from typing import List
from src.configuration.smtpconfig import SmtpConfig
from src.configuration.domain import DomainConfig
import sys
from datetime import datetime

def generate_message_id(suffix=f"@{DomainConfig.domain}"):
    if not isinstance(suffix, str):
        suffix = str(suffix)

    return "".join(["<", str(uuid.uuid4()) + suffix, ">"])

def send_mail(mail_from: str, rcpt_to: List[str], payload: str):
    uniq_id = generate_message_id()
    body = f"Message-ID: {uniq_id}"
    date = datetime.now().strftime("%a, %d %b %Y %T +0700")
    payload = body + "\n" + "Date: " + date + "\n" + payload
    if SmtpConfig.mode == "ssl":
        smtp = smtplib.SMTP_SSL(SmtpConfig.host, SmtpConfig.port)
    else:
        smtp = smtplib.SMTP(SmtpConfig.host, SmtpConfig.port)
        if SmtpConfig.mode == "tls":
            smtp.starttls()

    if SmtpConfig.user and SmtpConfig.password:
        if sys.version_info < (3, 0):
            # python 2.x
            # login and password must be encoded
            # because HMAC used in CRAM_MD5 require non unicode string
           smtp.login(
                smtp_login.encode("utf-8"), smtp_password.encode("utf-8")
            )
        else:
            # python 3.x
            smtp.login(SmtpConfig.user, SmtpConfig.password)
    try:
        payload = payload.encode("utf-8")
        ret = smtp.sendmail(mail_from, rcpt_to, payload)
#        print (payload)
    finally:
        try:
            smtp.quit()
        except Exception as e:
            print("ERROR - %s", e)

    return ret
