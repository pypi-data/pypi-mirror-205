from abc import ABC
from typing import Any, TypeVar
from pydantic import BaseModel as BM

T = TypeVar('T')

class GetResponseHandlerException(Exception):
    def __init__(self, response:dict, responses_handlers:list):
        self.response = response
        self.responses_handlers = responses_handlers

    def __str__(self) -> str:
        return (f'It is not possible to process the response with handlers: {self.responses_handlers}\n' +
                f'response: {self.response}')

class BaseMethod:
    def __init__(self, vk) -> None:
        self.vk = vk

    async def _method(self, method:str, **params):
        try:
            params.pop('self')
        except: pass
        return await self.vk.call_method(method, **params)

class Int:
    @classmethod
    def parse_obj(cls, obj:int):
        return int(obj)

class Bool:
    @classmethod
    def parse_obj(cls, obj:bool):
        return bool(obj)

class Str:
    @classmethod
    def parse_obj(cls, obj:str):
        return str(obj)

class BaseList(BM):
    __root__:list

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class BaseEvent(BM):
    raw:dict
    group_id:int
    v:str
    object:Any # ЗАГЛУШКА

    @property
    def type(self):
        return type(self)


class BaseRule(ABC):
    def __init__(self, vk, event):
        self.vk = vk
        self.event = event

class BaseDispatcher(ABC):
    def __init__(self, vk) -> None:
        self.vk = vk

__all__ = ('BaseMethod', 'BaseList', 'BaseEvent')
