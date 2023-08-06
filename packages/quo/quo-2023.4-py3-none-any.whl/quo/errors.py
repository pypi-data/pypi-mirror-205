import typing as ty
import gettext
import os

from quo.accordance import filename_to_ui, get_text_stderr

_ = gettext.gettext


def _join_param_hints(param_hint):
    if isinstance(param_hint, (tuple, list)):
        return " / ".join(repr(x) for x in param_hint)
    return param_hint


class Outlier(Exception):
    """An exception that Quo can handle and show to the user."""

    #: The exit code for this exception.
    exit_code = 1

    def __init__(self, message: ty.Optional[str]):
        super().__init__(message)
        print("\a")
        self.message = message

    def format_message(self):
        return self.message

    def __str__(self):
        return self.message

    def show(self, file=None):
        from .expediency.vitals import inscribe

        if file is None:
            file = get_text_stderr()
        inscribe(_(f"Error: {self.format_message()}", file=file))


class ValidationError(Outlier):
    """
    Error raised by :meth:`.Validator.validate`.
    :param line: The cursor position where the error occurred.
    :param message: Text.
    """

    def __init__(self, line: int = 0, message: str = "") -> None:
        super().__init__(message)
        self.line = line
        self.message = message

    def __repr__(self) -> str:
        return "_%s(line=%r, message=%r)" % (
            self.__class__.__name__,
            self.line,
            self.message,
        )


class LayoutError(Outlier):
    pass


class UsageError(Outlier):
    """An internal exception that signals a usage error.This typically aborts any further handling.

    :param message: the error message to display.
    :param clime: optionally the context that caused this error.  Quo will fill in the context automatically in some situations.
    """

    exit_code = 2

    def __init__(self, message: ty.Optional[str], clime=None):
        super().__init__(message)
        self.clime = clime
        self.cmd = self.clime.command if self.clime else None

    def show(self, file=None):
        from .expediency.vitals import inscribe

        if file is None:
            file = get_text_stderr()
        color = None
        hint = ""
        if self.cmd is not None and self.cmd.get_autohelp(self.clime) is not None:
            hint = (
                f"Try '{self.clime.command_path}"
                f" {self.clime.autohelp_names[0]}' for help.\n"
            )
        if self.clime is not None:
            color = self.clime.color
            inscribe(f"{self.clime.get_usage()}\n{hint}", file=file, color=color)
        inscribe(f"Error: {self.format_message()}", file=file, color=color)


class NoConsoleScreenBufferError(Outlier):
    """
    Raised when the application is not running inside a Windows Console, but the user tries to instantiate Win32Output.
    """

    def __init__(self) -> None:
        # Are we running in 'xterm' on Windows, like git-bash for instance?
        xterm = "xterm" in os.environ.get("TERM", "")
        if xterm:
            message = (
                "Found %s, while expecting a Windows console. "
                'Maybe try to run this program using "winpty" '
                "or run it in cmd.exe instead. Or otherwise, "
                "in case of Cygwin, use the Python executable "
                "that is compiled for Cygwin." % os.environ["TERM"]
            )
        else:
            message = "No Windows console found. Are you running cmd.exe?"
            super().__init__(message)


class BadParameter(UsageError):
    """This exception formats out a standardized error message for a bad parameter.


    :param param: the parameter object that caused this error.  This can be left out, and Quo will attach this info itself if possible.
    :param param_hint: a string that shows up as parameter name.This can be used as alternative to `param` in cases where custom validation should happen.  If it is a string it's used as such, if it's a list then each item is quoted and separated.
    """

    def __init__(
        self,
        message: ty.Optional[str],
        clime=None,
        param: ty.Optional["Parameter"] = None,
        param_hint=None,
    ):
        super().__init__(message, clime)
        self.param = param
        self.param_hint = param_hint

    def format_message(self):
        if self.param_hint is not None:
            param_hint = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.clime)
        else:
            return f"Invalid value: {self.message}"
        param_hint = _join_param_hints(param_hint)

        return f"Invalid value for {param_hint}: {self.message}"


class MissingParameter(BadParameter):
    """This parameter is raised if Quo required an app or argument but it was not provided.

    :param param_type: a string that indicates the type of the parameter.The default is to inherit the parameter type from the given `param`.  Valid values are ``'parameter'``,``'app'`` or ``'arg'``.
    """

    def __init__(
        self,
        message: ty.Optional[str] = None,
        clime=None,
        param: ty.Optional["Parameter"] = None,
        param_hint=None,
        param_type=None,
    ):
        super().__init__(message, clime, param, param_hint)
        self.param_type = param_type

    def format_message(self):
        if self.param_hint is not None:
            param_hint = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.clime)
        else:
            param_hint = None
        param_hint = _join_param_hints(param_hint)

        param_type = self.param_type
        if param_type is None and self.param is not None:
            param_type = self.param.param_type_name

        msg = self.message
        if self.param is not None:
            msg_extra = self.param.type.get_missing_message(self.param)
            if msg_extra:
                if msg:
                    msg += f".  {msg_extra}"
                else:
                    msg = msg_extra

        hint_str = f" {param_hint}" if param_hint else ""
        return f"Missing {param_type}{hint_str}.{' ' if msg else ''}{msg or ''}"

    def __str__(self):
        if self.message is None:
            param_name = self.param.name if self.param else None
            return f"missing parameter: {param_name}"
        else:
            return self.message


class NoSuchApp(UsageError):
    """Raised if Quo attempted to handle an app that does not
    exist.

    """

    def __init__(
        self, appname, message: ty.Optional[str] = None, possibilities=None, clime=None
    ):
        if message is None:
            message = f"{appname}"

        super().__init__(message, clime)
        self.appname = appname
        self.possibilities = possibilities

    def format_message(self):
        bits = [self.message]
        if self.possibilities:
            if len(self.possibilities) == 1:
                bits.append(f"Did you mean {self.possibilities[0]}?")
            else:
                possibilities = sorted(self.possibilities)
                bits.append(f"(Possible apps: {', '.join(possibilities)})")
        return "  ".join(bits)


class BadAppUsage(UsageError):
    """Raised if an app is generally supplied but the use of the app was incorrect.  This is for instance raised if the number of arguments for an app is not correct.

    :param appname: the name of the app being used incorrectly.
    """

    def __init__(self, appname, message, clime=None):
        super().__init__(message, clime)
        self.appname = appname


class BadArgUsage(UsageError):
    """Raised if an arg is generally supplied but the use of the argument was incorrect.  This is for instance raised if the number of values for an arg is not correct."""


class FileError(Outlier):
    """Raised if a file cannot be opened."""

    def __init__(self, filename, hint=None):
        ui_filename = filename_to_ui(filename)
        if hint is None:
            hint = "unknown error"

        super().__init__(hint)
        self.ui_filename = ui_filename
        self.filename = filename

    def format_message(self):
        return f"Could not open file {self.ui_filename}: {self.message}"


class Abort(RuntimeError):
    """An internal signalling exception that signals Quo to abort."""


class Exit(RuntimeError):
    """An exception that indicates that the application should exit with some status code.

    :param code: the status code to exit with.
    """

    __slots__ = ("exit_code",)

    def __init__(self, code: ty.Optional[int] = 0):
        self.exit_code = code


class HeightIsUnknownError(Outlier):
    # used in quo.renderer
    "Information unavailable. Did not yet receive the CPR response."



class ClipboardError(Outlier):
    pass
    
    
class ArgumentError(Exception):
    """An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(self, argument, message):
        self.argument_name = _get_action_name(argument)
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = '%(message)s'
        else:
            format = 'argument %(argument_name)s: %(message)s'
        return format % dict(message=self.message,
                             argument_name=self.argument_name)


class ArgumentTypeError(Exception):
    """An error from trying to convert a command line string to a type."""
    pass

