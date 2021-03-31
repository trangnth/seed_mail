import argparse

parser = argparse.ArgumentParser()
arg = parser.add_mutually_exclusive_group()
arg.add_argument(
    "-s",
    "--send",
    type=int,
    default=0,
    help="send X messages (default: X = 0)",
)

arg.add_argument(
    "-a",
    "--add",
    type=int,
    default=0,
    help="add X messages to sent folder (default: X = 0)",
)

arg.add_argument(
    "-n",
    "--new",
    type=int,
    default=0,
    help="imap new X messages (default: X = 0)",
)
args = parser.parse_args()
