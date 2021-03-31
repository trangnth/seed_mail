from operator import ge
import sys
import time
import argparse

import asyncio
import threading

from imapclient.response_parser import parse_response

from src.libs.logger import logger
from src.libs.arguments import args
from src.libs.client import imap, smtp
from src.configuration.smtpconfig import SmtpConfig
from src.configuration.imapconfig import ImapConfig

sys.tracebacklimit = 0


def send_new_message():
    logger.info("Main thread name: {}"
                .format(threading.current_thread().name))
    rcpt_to = SmtpConfig.rcpt_to.split(",")
    smtp.send_mail(SmtpConfig.user, rcpt_to, SmtpConfig.payload)


def imap_add_message_to_sent():
    logger.info("Main thread name: {}"
                .format(threading.current_thread().name))
    client = imap.new_imap_client()
    imap.login(client)
    imap.send_message(client, ImapConfig.payload)


def imap_new_message():
    logger.info("Main thread name: {}"
                .format(threading.current_thread().name))
    client = imap.new_imap_client()
    imap.login(client)
    imap.new_message(client)


def get_arg(send, add, new):
    mapping_func = {
        send: send_new_message,
        add: imap_add_message_to_sent,
        new: imap_new_message
    }
    number_of_message = max(mapping_func.keys())
    func = mapping_func.get(number_of_message)
    return number_of_message, func


async def main(number_of_message, func):
    loop = asyncio.get_running_loop()
    for _ in range(number_of_message):
        loop.run_in_executor(None, func)


if __name__ == '__main__':
    number_of_message, func = get_arg(**args.__dict__)
    s = time.perf_counter()
    asyncio.run(main(number_of_message, func))
    elapsed = time.perf_counter() - s
    logger.info(f"{__file__} EXECUTED IN {elapsed:0.5f} SECONDS.")