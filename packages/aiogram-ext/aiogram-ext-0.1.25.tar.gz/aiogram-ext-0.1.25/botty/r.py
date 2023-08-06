from dataclasses import dataclass

from botty import Query, Message
from .helpers import reply, edit
from .keyboards import ReplyMarkup


@dataclass
class Answer:
    text: str
    markup: ReplyMarkup | bool = None


def r(event: Message | Query, answer: Answer):
    return reply(event, answer.text, answer.markup)


def e(event: Message | Query, answer: Answer):
    return edit(event, answer.text, answer.markup)
