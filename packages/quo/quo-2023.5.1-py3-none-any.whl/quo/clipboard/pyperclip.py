from typing import Optional

from quo.selection import SelectionType

from .core import Clipboard, Data

#try:
#    import pyperclip

#except ModuleNotFoundError:
 #   import os
 #   os.system("pip install -U pyperclip")

#__all__ = [
 #   "PyperclipClipboard",
#]

# We will be deprecating this in the later versions..

class PyperClipboard(Clipboard):
    """
    Clipboard that synchronizes with the Windows/Mac/Linux system clipboard,
    using the pyperclip module.
    """

    def __init__(self) -> None:
        self._data: Optional[Data] = None

    def set_data(self, data: Data) -> None:
        self._data = data
      #  pyperclip.copy(data.text)

    def get_data(self) -> Data:
    #    text = pyperclip.paste()

        # When the clipboard data is equal to what we copied last time, reuse
        # the `Data` instance. That way we're sure to keep the same
        # `SelectionType`.
        if self._data and self._data.text == text:
            return self._data

        # Pyperclip returned something else. Create a new instance of `Data`
        else:
            return Data(
                text=text,
                type=SelectionType.LINES if "\n" in text else SelectionType.CHARACTERS,
            )
