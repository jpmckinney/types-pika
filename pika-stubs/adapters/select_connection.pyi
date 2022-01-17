from __future__ import annotations

import abc
from collections.abc import Sequence
from typing import IO
from typing import Any
from typing import AnyStr
from typing import Callable

from .. import compat
from .. import connection
from . import base_connection
from .utils import connection_workflow
from .utils import nbio_interface
from .utils import selector_ioloop_adapter

SELECT_TYPE: str | None

_OnCloseCallback = Callable[[base_connection.BaseConnection, Exception], None]
_OnOpenCallback = Callable[[base_connection.BaseConnection], None]
_OnOpenErrorCallback = Callable[[base_connection.BaseConnection, str | Exception], None]

class SelectConnection(base_connection.BaseConnection[IOLoop]):
    def __init__(
        self,
        parameters: connection.Parameters | None = ...,
        on_open_callback: _OnOpenCallback | None = ...,
        on_open_error_callback: _OnOpenErrorCallback | None = ...,
        on_close_callback: _OnCloseCallback | None = ...,
        custom_ioloop: IOLoop | nbio_interface.AbstractIOServices | None = ...,
        internal_connection_workflow: bool = ...,
    ) -> None: ...
    @classmethod
    def create_connection(
        cls,
        connection_configs: Sequence[connection.Parameters],
        on_done: Callable[
            [
                connection.Connection
                | connection_workflow.AMQPConnectionWorkflowFailed
                | connection_workflow.AMQPConnectionWorkflowAborted
            ],
            None,
        ],
        custom_ioloop: IOLoop | None = ...,
        workflow: connection_workflow.AbstractAMQPConnectionWorkflow | None = ...,
    ) -> connection_workflow.AbstractAMQPConnectionWorkflow: ...

class _Timeout:

    deadline: float = ...
    callback: Callable[[], None] = ...
    def __init__(self, deadline: float, callback: Callable[[], None]) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

class PollEvents:

    READ: int = ...
    WRITE: int = ...
    ERROR: int = ...

class IOLoop(selector_ioloop_adapter.AbstractSelectorIOLoop[_Timeout]):

    READ: int = ...
    WRITE: int = ...
    ERROR: int = ...
    def __init__(self) -> None: ...
    def close(self) -> None: ...
    def call_later(self, delay: float, callback: Callable[[], None]) -> _Timeout: ...
    def remove_timeout(self, timeout_handle: _Timeout) -> None: ...
    def add_callback_threadsafe(self, callback: Callable[[], None]) -> None: ...
    def add_callback(self, callback: Callable[[], None]) -> None: ...
    def process_timeouts(self) -> None: ...
    def add_handler(self, fd: IO[AnyStr], handler: Callable[[IO[AnyStr], int], None], events: int) -> None: ...
    def update_handler(self, fd: IO[AnyStr], events: int) -> None: ...
    def remove_handler(self, fd: IO[AnyStr]) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def activate_poller(self) -> None: ...
    def deactivate_poller(self) -> None: ...
    def poll(self) -> None: ...

class _PollerBase(compat.AbstractBase):

    POLL_TIMEOUT_MULT: int = ...
    def __init__(self, get_wait_seconds: Callable[[], float], process_timeouts: Callable[[], None]) -> None: ...
    def close(self) -> None: ...
    def wake_threadsafe(self) -> None: ...
    def add_handler(self, fileno: int, handler: Callable[[int, int], None], events: int) -> None: ...
    def update_handler(self, fileno: int, events: int) -> None: ...
    def remove_handler(self, fileno: int) -> None: ...
    def activate_poller(self) -> None: ...
    def deactivate_poller(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @abc.abstractmethod
    def poll(self) -> None: ...

class SelectPoller(_PollerBase):

    POLL_TIMEOUT_MULT: int = ...
    def poll(self) -> None: ...

class KQueuePoller(_PollerBase):
    def __init__(self, get_wait_seconds: Callable[[], float], process_timeouts: Callable[[], None]) -> None: ...
    def poll(self) -> None: ...

class PollPoller(_PollerBase):

    POLL_TIMEOUT_MULT: int = ...
    def __init__(self, get_wait_seconds: Callable[[], float], process_timeouts: Callable[[], None]) -> None: ...
    def poll(self) -> None: ...

class EPollPoller(PollPoller):

    POLL_TIMEOUT_MULT: int = ...
