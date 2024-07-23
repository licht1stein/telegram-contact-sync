import argparse
import csv
import uuid

from telethon.sync import TelegramClient
from telethon import functions, types

NAME = "telegram-client-sync"


def read_csv(filename):
    with open(filename, newline="") as csvfile:
        return list(csv.reader(csvfile))[1:]


def prepare_contacts(contacts_data):
    return [
        types.InputPhoneContact(
            client_id=0, phone=phone[0], first_name=str(uuid.uuid4()), last_name=""
        )
        for phone in contacts_data
    ]


def add_contacts(api_id, api_hash, contacts):
    with TelegramClient(NAME, api_id, api_hash) as client:
        result = client(functions.contacts.ImportContactsRequest(contacts=contacts))
        print(result.stringify())


def make_parser():
    parser = argparse.ArgumentParser(prog="Telegram Contacts Importer")
    parser.add_argument("filename")
    parser.add_argument("-i", "--api_id", type=int, required=True)
    parser.add_argument("-s", "--api_hash", required=True)
    return parser


def run():
    parser = make_parser()
    args = parser.parse_args()
    data = read_csv(args.filename)
    contacts = prepare_contacts(data)
    add_contacts(args.api_id, args.api_hash, contacts)


if __name__ == "__main__":
    run()
