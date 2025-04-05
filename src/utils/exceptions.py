from dataclasses import dataclass


@dataclass(frozen=True)
class EmptyMsgTelegram(Exception):
    """Ошибка пустого месседжа в сообщении телеги."""

    message_id: str | None = '<не передано>'
    type_msg: str = 'Инлайн'

    @property
    def message(self):
        return f'{self.type_msg} сообщение id: {self.message_id} пустое!'

    def __str__(self):
        return self.message
