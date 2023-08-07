"""
Key bindings for extra page navigation: bindings for up/down scrolling through
long pages, like in Emacs or Vi.
"""
from quo.filters import buffer_has_focus, emacs_mode, vi_mode
from quo.keys import KeyBinder
from quo.keys.key_binding.key_bindings import (
    ConditionalKeyBindings,
    KeyBindingsBase,
    merge_key_bindings,
)

from .scroll import (
    scroll_backward,
    scroll_forward,
    scroll_half_page_down,
    scroll_half_page_up,
    scroll_one_line_down,
    scroll_one_line_up,
    scroll_page_down,
    scroll_page_up,
)

__all__ = [
    "load_page_navigation_bindings",
    "load_emacs_page_navigation_bindings",
    "load_vi_page_navigation_bindings",
]


def load_page_navigation_bindings() -> KeyBindingsBase:
    """
    Load both the Vi and Emacs bindings for page navigation.
    """
    # Only enable when a `Buffer` is focused, otherwise, we would catch keys
    # when another widget is focused (like for instance `c-d` in a
    # ptterm.Terminal).
    return ConditionalKeyBindings(
        merge_key_bindings(
            [
                load_emacs_page_navigation_bindings(),
                load_vi_page_navigation_bindings(),
            ]
        ),
        buffer_has_focus,
    )


def load_emacs_page_navigation_bindings() -> KeyBindingsBase:
    """
    Key bindings, for scrolling up and down through pages.
    This are separate bindings, because GNU readline doesn't have them.
    """
    key_bindings = KeyBinder()
    handle = key_bindings.add

    handle("ctrl-v")(scroll_page_down)
    handle("pagedown")(scroll_page_down)
    handle("escape", "v")(scroll_page_up)
    handle("pageup")(scroll_page_up)

    return ConditionalKeyBindings(key_bindings, emacs_mode)


def load_vi_page_navigation_bindings() -> KeyBindingsBase:
    """
    Key bindings, for scrolling up and down through pages.
    This are separate bindings, because GNU readline doesn't have them.
    """
    key_bindings = KeyBinder()
    handle = key_bindings.add

    handle("ctrl-f")(scroll_forward)
    handle("ctrl-b")(scroll_backward)
    handle("ctrl-d")(scroll_half_page_down)
    handle("ctrl-u")(scroll_half_page_up)
    handle("ctrl-e")(scroll_one_line_down)
    handle("ctrl-y")(scroll_one_line_up)
    handle("pagedown")(scroll_page_down)
    handle("pageup")(scroll_page_up)

    return ConditionalKeyBindings(key_bindings, vi_mode)
