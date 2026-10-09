"""Feature String (FeatStr) DSL.

FeatStr is a tiny declarative language used to enable or disable named
features. It is primarily intended for command-line flags and configuration
overrides.

Grammar:

    featstr := item ("," item)*

    item :=
        NAME        -- enable feature
      | "+" NAME    -- explicitly enable feature
      | "-" NAME    -- disable feature
      | "full"      -- initialize with schema defaults
      | "none"      -- initialize with inverted schema defaults

Example:

    lsp,ts,-plg
    none,+lsp,+ts
    full,-fmt,-plg

Result:

    parse() returns a feature mask:

        {
            "lsp": True,
            "fmt": False,
            "ts": False,
            "plg": False,
        }
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

__all__ = ["parse"]


def _noop(_msg: str) -> None:
    """Default error handler: silently ignore errors."""


def parse(
    feat_s: str,
    defaults: Mapping[str, bool],
    on_error: Callable[[str], None] | None = None,
) -> dict[str, bool]:
    """Parse a feature string.

    ``+foo,-bar,baz`` means enable ``foo`` and ``baz``, and disable ``bar``.
    The keyword ``full`` means use the full default options, ``none`` means
    use the *not* of the default options.

    Args:
        feat_s: feature string.
        defaults: schema table.
        on_error: optional error callback.

    Returns:
        The masked result.
    """
    mask: dict[str, bool] = {}
    if on_error is None:
        on_error = _noop

    for feat_item in feat_s.split(","):
        # Lua's `string.gmatch(feat_s, '([^,]+)')` never yields empty
        # items (e.g. "a,,b" -> "a", "b"); mirror that by skipping
        # empty split results.
        if not feat_item:
            continue

        feat_item = feat_item.strip()
        first_char = feat_item[:1]

        if feat_item == "full":
            for k, v in defaults.items():
                mask[k] = v
        elif feat_item == "none":
            for k, v in defaults.items():
                mask[k] = not v
        else:
            if first_char in ("+", "-"):
                feat_name = feat_item[1:]
            else:
                feat_name = feat_item

            if feat_name not in defaults:
                on_error(f"Unknown feature: {feat_name}")
            elif first_char == "-":
                mask[feat_name] = False
            else:
                # Both bare `NAME` and `+NAME` enable the feature.
                mask[feat_name] = True

    return mask
