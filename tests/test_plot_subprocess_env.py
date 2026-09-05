"""Tests for qlinterface._plot_subprocess_env().

Why this exists: a conda interpreter's bundled libstdc++ shadows the system
one that Mesa's DRI drivers are built against, so every PyVista/VTK (3D)
ql-* script aborts with "Cannot create GLX context" while every
matplotlib-based one keeps working. execute_script() compensates by
prepending the system libstdc++ to the child's LD_PRELOAD. The condition
that triggers that is environment-dependent and cannot be exercised on a
machine that doesn't happen to have the broken combination, so it is tested
here against a fabricated filesystem/platform instead - no rendering, no
subprocess.
"""
import os
import sys

import pytest

from interfacetk import qlinterface


SYSTEM = "/usr/lib/x86_64-linux-gnu/libstdc++.so.6"


@pytest.fixture
def fake_env(monkeypatch):
    """Pretend to be Linux, with a controllable set of existing files and a
    controllable starting environment."""
    def setup(present, platform="linux", environ=None):
        monkeypatch.setattr(sys, "platform", platform)
        monkeypatch.setattr(sys, "prefix", "/opt/conda")
        monkeypatch.setattr(os.path, "exists", lambda p: p in present)
        monkeypatch.setattr(os, "environ", dict(environ or {}))
    return setup


def test_preloads_the_system_library_under_conda(fake_env):
    fake_env({"/opt/conda/lib/libstdc++.so.6", SYSTEM})
    env, note = qlinterface._plot_subprocess_env()
    assert env["LD_PRELOAD"] == SYSTEM
    assert note and SYSTEM in note
    assert note.startswith("#")  # a comment block, written into the script's log


def test_does_nothing_without_a_bundled_library(fake_env):
    """A system-Python install has no conda copy to shadow the system one."""
    fake_env({SYSTEM})
    env, note = qlinterface._plot_subprocess_env()
    assert "LD_PRELOAD" not in env
    assert note is None


def test_does_nothing_when_the_system_library_is_missing(fake_env):
    fake_env({"/opt/conda/lib/libstdc++.so.6"})
    env, note = qlinterface._plot_subprocess_env()
    assert "LD_PRELOAD" not in env
    assert note is None


@pytest.mark.parametrize("platform", ["darwin", "win32"])
def test_does_nothing_off_linux(fake_env, platform):
    """Neither macOS nor Windows uses LD_PRELOAD or Mesa DRI drivers."""
    fake_env({"/opt/conda/lib/libstdc++.so.6", SYSTEM}, platform=platform)
    env, note = qlinterface._plot_subprocess_env()
    assert "LD_PRELOAD" not in env
    assert note is None


def test_preserves_an_existing_preload(fake_env):
    fake_env({"/opt/conda/lib/libstdc++.so.6", SYSTEM},
             environ={"LD_PRELOAD": "/somewhere/libfoo.so"})
    env, _ = qlinterface._plot_subprocess_env()
    assert env["LD_PRELOAD"] == SYSTEM + ":/somewhere/libfoo.so"


def test_leaves_a_users_own_choice_alone(fake_env):
    """Already preloaded by the user - don't duplicate it."""
    fake_env({"/opt/conda/lib/libstdc++.so.6", SYSTEM},
             environ={"LD_PRELOAD": SYSTEM})
    env, note = qlinterface._plot_subprocess_env()
    assert env["LD_PRELOAD"] == SYSTEM
    assert note is None
