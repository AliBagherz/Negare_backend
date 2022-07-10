import base64


def get_chat_text(user1: int, user2: int) -> str:
    if user1 < user2:
        smaller = user1
        bigger = user2
    elif user2 < user1:
        smaller = user2
        bigger = user1
    else:
        raise Exception("user ids couldn't be same")
    return str(smaller) + '-' + str(bigger)


def encode_text(message: str) -> str:
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def decode_text(base64_message: str) -> str:
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')


def get_chat_code(user1: int, user2: int) -> str:
    return encode_text(get_chat_text(user1, user2))


def get_users_from_code(chat_code: str) -> list:
    smaller, bigger = map(int, chat_code.split('-'))
    return [smaller, bigger]
