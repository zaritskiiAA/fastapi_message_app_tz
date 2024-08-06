def text_cannot_be_null(value: str):
    assert value, 'Для отправки сообщения необходимо указать минимум 1 символ.'
    return value