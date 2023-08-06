from dataclasses import dataclass

from botty import Query, Message
from .helpers import reply
from .keyboards import ReplyMarkup


@dataclass
class Answer:
    text: str
    markup: ReplyMarkup | bool = None


def r(event: Message | Query, answer: Answer):
    return reply(event, answer.text, answer.markup)
