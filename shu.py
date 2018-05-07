#!/usr/bin/env python3
import logging
import sys

import socks
import yaml
from telethon import TelegramClient, events

from secret import api_hash, api_id

_logger = logging.getLogger(__name__)


def read_config(filename='config.yml'):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)

    return config


def user_matches(user, rules):
    for rule in rules:
        matches = True

        for attr in rule:
            if attr.startswith('_'):
                continue

            user_attr = getattr(user, attr, False)

            if user_attr and user_attr != rule[attr]:
                break
        else:
            return rule
    else:
        return False


def handler(msg_event):
    try:
        config = read_config()
        user = client.get_entity(msg_event.input_sender)

        if msg_event.is_private:
            chatname = user.username
        else:
            chatname = client.get_entity(msg_event.input_chat).title

        rules = config["Chats"].get(chatname, None)

        if rules is None:
            _logger.debug("No rules for this message")
            return

        rule = user_matches(user, rules)

        if rule:
            if rule["_action"] == "print":
                username = user.username
                if username is None:
                    username = "{0} {1}".format(user.second_name, user.first_name)
                _logger.info("[User] = %s [Chat] = %s [Rule] = %s", username, chatname, rule)
            elif rule["_action"] == "delete":
                _logger.info("DELETE: %s", rule)
                client.delete_messages(chatname, msg_event.message)
            elif rule["_action"] == "autoread":
                _logger.info("AUTOREAD: %s", rule)
                client.send_read_acknowledge(chatname, msg_event.message)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    client = TelegramClient(
        'clientor',
        api_id,
        api_hash,
        # Useful if you live in Russia
        # proxy=(socks.SOCKS5, '127.0.0.1', 9150),
        update_workers=1,
        spawn_read_thread=False
    )
    client.start()

    logging.basicConfig(level=logging.INFO)
    client.on(events.NewMessage)(handler)
    client.idle()
