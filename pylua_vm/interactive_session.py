"""
InteractiveSession: Persistent interactive Lua VM session with PTY and threading support.
"""
import os
import pty
import threading
import queue
import subprocess
import select
import time

class InteractiveSession:
    """
    Manages a persistent interactive Lua interpreter process using PTY.
    Provides bidirectional I/O and real-time output streaming.
    """
    def __init__(self, lua_executable="lua", name="InteractiveLuaVM"):
        self.lua_executable = lua_executable
        self.name = name
        self.process = None
        self.master_fd = None
        self.slave_fd = None
        self.output_queue = queue.Queue()
        self._output_thread = None
        self._running = False

    def start(self):
        if self._running:
            raise RuntimeError("Session already running")
        self.master_fd, self.slave_fd = pty.openpty()
        self.process = subprocess.Popen(
            [self.lua_executable],
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            bufsize=0,
            close_fds=True
        )
        self._running = True
        self._output_thread = threading.Thread(target=self._read_output, daemon=True)
        self._output_thread.start()

    def _read_output(self):
        while self._running:
            rlist, _, _ = select.select([self.master_fd], [], [], 0.1)
            if self.master_fd in rlist:
                try:
                    data = os.read(self.master_fd, 1024)
                    if data:
                        self.output_queue.put(data.decode(errors="replace"))
                except OSError:
                    break
            time.sleep(0.01)

    def send_input(self, input_str):
        if not self._running:
            raise RuntimeError("Session not running")
        os.write(self.master_fd, input_str.encode())

    def read_output(self, timeout=0.1):
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self):
        self._running = False
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=2)
        if self.master_fd:
            os.close(self.master_fd)
        if self.slave_fd:
            os.close(self.slave_fd)
        self.process = None
        self.master_fd = None
        self.slave_fd = None

    def is_running(self):
        return self._running and self.process and self.process.poll() is None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
