from abc import abstractmethod
import sqlite3
from typing import Protocol
from tgmount import config
from tgmount.tgclient import MessageProto

""" 
Fetcher cache can be used when:
1. no limit specified
2. no max_id specified
"""


class TelegramMessagesFetcherCacheProto(Protocol):
    @abstractmethod
    async def message_source_config(self) -> config.MessageSource:
        pass

    @abstractmethod
    async def get_messages(self) -> list[MessageProto]:
        pass


class TelegramMessagesFetcherCache:
    """ """

    @staticmethod
    def load(filename: str):
        pass

    def __init__(
        self,
        message_source_config: config.MessageSource,
        database_connection: sqlite3.Connection,
    ) -> None:
        self._message_source_config = message_source_config
        self._database_connection = database_connection
