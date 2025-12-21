# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import os
import time
import threading
import subprocess
from typing import NoReturn

# local
import module
from basic import cwd


class Services (object):
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._instances: dict[str, Instance] = {}

    def instances_names(self) -> list[str]:
        with self._lock:
            return list(self._instances.keys())

    def instance(self, name: str) -> "Instance":
        with self._lock:
            return self._instances[name]

    def load(self) -> None:
        for filename in os.listdir(cwd.instances):
            if not filename.endswith(".toml"): continue
            path = os.path.join(cwd.instances, filename)
            if not os.path.isfile(path): continue
            name = os.path.splitext(filename)[0]

            with self._lock:
                if name not in self._instances:
                    self._instances[name] = Instance(name)


class Instance (object):
    def __init__(self, name: str) -> None:
        self.lock = threading.RLock()
        self.__name = name
        self.__config_file = os.path.join(cwd.instances, f"{name}.toml")
        self.process: subprocess.Popen | None = None
        self.thread_stdout: threading.Thread | None = None
        self.thread_stderr: threading.Thread | None = None
        self.logs: list[str] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def alive(self) -> bool:
        with self.lock:
            return self.process is not None and self.process.poll() is None

    def run(self) -> None:
        if self.alive: return

        with self.lock:
            if self.process is not None: return
            self.process = subprocess.Popen(
                [cwd.assets.frpc, "-c", self.__config_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.thread_stdout = threading.Thread(target=self._log_stdout, name=f"Instance[{self.__name}].stdout", daemon=True)
        self.thread_stderr = threading.Thread(target=self._log_stderr, name=f"Instance[{self.__name}].stderr", daemon=True)
        self.thread_stdout.start()
        self.thread_stderr.start()

    def stop(self) -> None:
        if not self.alive: return

        with self.lock:
            if self.process is None: return
            self.process.terminate()

    def add_log(self, content: str) -> None:
        while True:
            s = content.find("\033")
            if s == -1: break
            m = content[s:].find("[0m")
            if m == -1: break
            content = content[:s] + content[s+m+2:]

        with self.lock:
            self.logs.append(content)

    def _log_stdout(self) -> NoReturn:
        time.sleep(0.1)
        if self.process is None: raise SystemExit(0)
        if self.process.stdout is None: raise SystemExit(0)

        while self.alive:
            line = self.process.stdout.readline().decode("utf-8").strip()
            if line: self.add_log(line)

        raise SystemExit(0)

    def _log_stderr(self) -> NoReturn:
        time.sleep(0.1)
        if self.process is None: raise SystemExit(0)
        if self.process.stderr is None: raise SystemExit(0)

        while self.alive:
            line = self.process.stderr.readline().decode("utf-8").strip()
            if line: self.add_log(line)

        raise SystemExit(0)


def initialize_first() -> None:
    module.services = Services()


def initialize_final() -> None:
    module.services.load()
