import platform
from abc import ABC, abstractmethod

from dashscope.version import __version__


class BaseRequest(ABC):
    def __init__(self) -> None:
        ua = 'dashscope/%s; python/%s; platform/%s; processor/%s' % (
            __version__,
            platform.python_version(),
            platform.platform(),
            platform.processor(),
        )
        self.headers = {'user-agent': ua}

    @abstractmethod
    def call(self):
        raise NotImplementedError()


class AioBaseRequest(BaseRequest):
    @abstractmethod
    async def async_call(self):
        raise NotImplementedError()
