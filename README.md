# shuplpy

The utility is written to ignore non-relevant messages in radical way.

## Overview

The main principle is simple: specify `conditions` and corresponding `actions`. When the `condition` is met for some `message` the corresponding `action` is triggered.

`condition` + `action` is called `rule`. Rules are located in the file `config.yml`.

## Configuration syntax

**Important**: Conditions are case sensitive.

```yaml
Chats:
  <Chatname_1>:
    # Rule #1 for Chatname_1. I don't need his fucking messages in this chat
    - username: HateThisGuy
      _action: delete
    # Rule #2 for Chatname_1. Read the messages of this guy automatically 
    - username: TalksToMuch
      _action: autoread
  <Chatname_2>:
    # Rule #1 for Chatname_2. Just print some debug info when he sent a message
    - first_name: John
      second_name: Doe
      _action: print
  # Works in private messages too
  <SomeDude>:
    - _action: autoread
```

### Available conditions

- `username`
- `first_name`
- `second_name`
- actually you can specify here any field of `telethon.tl.types.User`, e.g. `phone: 79991234567` but it doesn't have much sense.

### Available actions
- `delete`: deletes `message` (only for you).
- `autoread`: automatically reads all messages in the chat up to the `message`.
- `print`: just prints a basic information about a `message`. Useful for debugging to see which messages are matched by your `contidion`.

## FAQ
Q: How the script is performing actions on my behalf?
A: By using Telegram API. You can read more [here](https://core.telegram.org/api/obtaining_api_id). Also you can obtain your `api_id` and `api_hash` at [https://my.telegram.org/apps](https://my.telegram.org/apps).

Q: I get an error: `ModuleNotFoundError: No module named 'secret'`. How can I fix it?
A: Create file `secret.py`. Then place here your `api_id` and `api_hash` from [https://my.telegram.org/apps](https://my.telegram.org/apps).
