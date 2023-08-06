from typing import Callable, Optional

from quo.text.core import AnyFormattedText
from quo.input import DummyInput
from quo.output import DummyOutput

from .console import Console

# __all__ = [
#    "DummyApplication",
# ]


class DummyApplication(Console[None]):
    """
    When no :class:`.Console` is running,
    :func:`.get_app` will run an instance of this :class:`.DummyApplication` instead.
    """

    def __init__(self) -> None:
        super().__init__(output=DummyOutput(), input=DummyInput())

    def run(
        self,
        pre_run: Optional[Callable[[], None]] = None,
        set_exception_handler: bool = True,
        in_thread: bool = False,
    ) -> None:
        raise NotImplementedError("A DummyApplication is not supposed to run.")

    async def run_async(
        self,
        pre_run: Optional[Callable[[], None]] = None,
        set_exception_handler: bool = True,
    ) -> None:
        raise NotImplementedError("A DummyApplication is not supposed to run.")

    async def run_system_command(
        self,
        command: str,
        wait_for_enter: bool = True,
        display_before_text: AnyFormattedText = "",
        wait_text: str = "",
    ) -> None:
        raise NotImplementedError

    def suspend_to_background(self, suspend_group: bool = True) -> None:
        raise NotImplementedError
