from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.client import CALPADS


class BaseAPIExt:
    def __init__(self, api: 'CALPADS'):
        self.api = api