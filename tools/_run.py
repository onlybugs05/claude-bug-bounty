"""Shared subprocess execution with process-group management.

Consolidates the ``run_cmd`` helpers from hunt.py and zero_day_fuzzer.py.

Usage:
    from tools._run import run_cmd
    ok, stdout = run_cmd("ls -la", timeout=30)
    ok, stdout, stderr = run_cmd("ls -la", timeout=30, split_stderr=True)
"""
from __future__ import annotations

import os
import signal
import subprocess


def run_cmd(
    cmd: str,
    *,
    cwd: str | None = None,
    timeout: int = 600,
    split_stderr: bool = False,
) -> tuple:
    """Run a shell command, returning its output.

    Uses ``os.setsid`` so that on timeout the entire child process tree
    is killed via ``os.killpg``, preventing orphan accumulation.

    Args:
        cmd:           Shell command string.
        cwd:           Working directory for the subprocess.
        timeout:       Seconds before the command is killed.
        split_stderr:  When *False* (default), stderr is merged into stdout
                       and the return is ``(success, combined_output)``.
                       When *True*, stderr is captured separately and the
                       return is ``(success, stdout, stderr)``.

    Returns:
        ``(bool, str)`` or ``(bool, str, str)`` depending on *split_stderr*.
    """
    proc = None
    stderr_mode = subprocess.PIPE if split_stderr else subprocess.STDOUT
    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=stderr_mode,
            text=True,
            cwd=cwd,
            preexec_fn=os.setsid,
        )
        stdout, stderr = proc.communicate(timeout=timeout)
        ok = proc.returncode == 0
        if split_stderr:
            return ok, stdout or "", stderr or ""
        return ok, stdout or ""
    except subprocess.TimeoutExpired:
        _kill(proc)
        if split_stderr:
            return False, "", "timeout"
        return False, "Command timed out"
    except Exception as e:
        _kill(proc)
        if split_stderr:
            return False, "", str(e)
        return False, str(e)


def _kill(proc: subprocess.Popen | None) -> None:
    """Kill the process group (or just the process) and reap."""
    if proc is None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        proc.kill()
    proc.wait()
