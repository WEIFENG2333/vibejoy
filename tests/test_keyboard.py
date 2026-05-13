from __future__ import annotations

import pytest

from vibejoy.keyboard import UnknownKeyError, is_known_key, resolve_key


class TestResolveKey:
    def test_single_char(self) -> None:
        assert resolve_key("a") == "a"
        assert resolve_key("5") == "5"
        assert resolve_key("/") == "/"

    def test_special_keys(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("enter") == Key.enter
        assert resolve_key("cmd") == Key.cmd
        assert resolve_key("shift") == Key.shift

    def test_aliases(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("return") == Key.enter
        assert resolve_key("option") == Key.alt
        assert resolve_key("esc") == Key.esc
        assert resolve_key("command") == Key.cmd

    def test_function_keys(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("f1") == Key.f1
        assert resolve_key("f20") == Key.f20

    def test_case_insensitive(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("ENTER") == Key.enter
        assert resolve_key("Cmd") == Key.cmd

    def test_unknown(self) -> None:
        with pytest.raises(UnknownKeyError):
            resolve_key("explode")


class TestSideExplicitModifiers:
    """Bare modifier names resolve to the left key; ``l_`` / ``r_`` prefixes
    pick a specific side. macOS distinguishes them, and pynput exposes
    ``*_r`` variants — surface that in the DSL so users can bind to a
    right-side modifier without dropping to raw pynput."""

    def test_bare_names_stay_left(self) -> None:
        from pynput.keyboard import Key

        # Backwards compat: ``cmd`` / ``shift`` / ``ctrl`` / ``alt`` / ``option``
        # have always meant the left key. New aliases must not change that.
        assert resolve_key("cmd") == Key.cmd
        assert resolve_key("shift") == Key.shift
        assert resolve_key("ctrl") == Key.ctrl
        assert resolve_key("alt") == Key.alt
        assert resolve_key("option") == Key.alt

    def test_left_prefix(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("l_cmd") == Key.cmd
        assert resolve_key("l_command") == Key.cmd
        assert resolve_key("l_shift") == Key.shift
        assert resolve_key("l_ctrl") == Key.ctrl
        assert resolve_key("l_control") == Key.ctrl
        assert resolve_key("l_alt") == Key.alt
        assert resolve_key("l_option") == Key.alt
        assert resolve_key("l_opt") == Key.alt

    def test_right_prefix(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("r_cmd") == Key.cmd_r
        assert resolve_key("r_command") == Key.cmd_r
        assert resolve_key("r_shift") == Key.shift_r
        assert resolve_key("r_ctrl") == Key.ctrl_r
        assert resolve_key("r_control") == Key.ctrl_r
        assert resolve_key("r_alt") == Key.alt_r
        assert resolve_key("r_option") == Key.alt_r
        assert resolve_key("r_opt") == Key.alt_r

    def test_side_prefix_case_insensitive(self) -> None:
        from pynput.keyboard import Key

        assert resolve_key("R_Option") == Key.alt_r
        assert resolve_key("L_SHIFT") == Key.shift


class TestIsKnownKey:
    def test_true_cases(self) -> None:
        assert is_known_key("enter")
        assert is_known_key("a")
        assert is_known_key("f5")

    def test_false_cases(self) -> None:
        assert not is_known_key("explode")
        assert not is_known_key("")
