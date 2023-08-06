from abc import ABC, abstractmethod


class BaseEmailProvider(ABC):
    adapter = None

    def __init__(self) -> None:
        assert self.adapter
        super().__init__()

    @abstractmethod
    def get_mailbox_list(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def create_mailbox(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_mailbox_information(self, *args, **kwargs):
        raise NotImplementedError()


class BaseAdapter(ABC):

    @abstractmethod
    def make_request(self, endpoint, body, method):
        raise NotImplementedError()

    @abstractmethod
    def _auth(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def _set_headers(self, *args, **kwargs):
        raise NotImplementedError()
