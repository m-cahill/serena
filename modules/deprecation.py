"""
Extension API deprecation helpers (Serena M25).

Import-light: stdlib only. Do not import ``script_callbacks`` here.
"""
from __future__ import annotations

import functools
import inspect
import warnings
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_DEPRECATION_PREFIX = "Serena extension API: "


def format_extension_api_deprecation(
    reason: str, version: str | None = None
) -> str:
    """Build canonical warning text (prefix + optional ``since`` clause)."""
    text = f"{_DEPRECATION_PREFIX}{reason}"
    if version is not None:
        text += f" (since {version})"
    return text


def warn_deprecated(reason: str, version: str | None = None) -> None:
    """Emit a :class:`DeprecationWarning` for extension API drift."""
    warnings.warn(
        format_extension_api_deprecation(reason, version),
        DeprecationWarning,
        stacklevel=2,
    )


def deprecated(reason: str, version: str | None = None) -> Callable[[F], F]:
    """
    Decorator: warn once per call to the wrapped function or class ``__init__``.

    Uses ``stacklevel=3`` so the reported caller is extension code invoking the
    deprecated callable, not the wrapper frame.
    """

    def decorator(target: F) -> F:
        if inspect.isclass(target):

            def _wrap_init(orig: Callable[..., Any]) -> Callable[..., Any]:
                @functools.wraps(orig)
                def wrapped(self: Any, *args: Any, **kwargs: Any) -> Any:
                    warnings.warn(
                        format_extension_api_deprecation(reason, version),
                        DeprecationWarning,
                        stacklevel=3,
                    )
                    return orig(self, *args, **kwargs)

                return wrapped

            wrapped_init = _wrap_init(target.__init__)
            target.__init__ = wrapped_init  # type: ignore[method-assign]
            return target

        @functools.wraps(target)
        def wrapped_fn(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                format_extension_api_deprecation(reason, version),
                DeprecationWarning,
                stacklevel=3,
            )
            return target(*args, **kwargs)

        return wrapped_fn  # type: ignore[return-value]

    return decorator
