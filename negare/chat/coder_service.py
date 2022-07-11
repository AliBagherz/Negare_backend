def get_users_from_code(chat_code: str) -> list:
    smaller, bigger = map(int, chat_code.split('-'))
    return [smaller, bigger]
