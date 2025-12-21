# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import os
import time
import toml
import tomllib
import threading
import subprocess
from typing import NoReturn

# local
import core
import module

from basic import cwd
from constants.event import INSTANCE_SWITCHED, INSTANCE_LOG_UPDATED


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

    def create(self, name: str) -> None:
        with self._lock:
            if name in self._instances: return
            self._instances[name] = Instance(name)

    def delete(self, name: str) -> None:
        with self._lock:
            if name not in self._instances: return
            instance = self.instance(name)
            if instance.alive: return
            os.remove(instance._config_file)
            del self._instances[name]


class Instance (object):
    def __init__(self, name: str) -> None:
        self.lock = threading.RLock()
        self._name = name
        self._config_file = os.path.join(cwd.instances, f"{name}.toml")
        self.process: subprocess.Popen | None = None
        self.thread_stdout: threading.Thread | None = None
        self.thread_stderr: threading.Thread | None = None
        self._logs: list[str] = []
        self._log_index = 0
        self.load_config()

    @property
    def name(self) -> str:
        return self._name

    @property
    def alive(self) -> bool:
        with self.lock:
            return self.process is not None and self.process.poll() is None

    def run(self) -> None:
        if self.alive: return

        with self.lock:
            self.process = subprocess.Popen(
                [cwd.assets.frpc, "-c", self._config_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        core.event.emit(INSTANCE_SWITCHED)
        self.thread_stdout = threading.Thread(target=self._log_stdout, name=f"Instance[{self._name}].stdout", daemon=True)
        self.thread_stderr = threading.Thread(target=self._log_stderr, name=f"Instance[{self._name}].stderr", daemon=True)
        self.thread_stdout.start()
        self.thread_stderr.start()

    def reload(self) -> None:
        subprocess.getoutput(f"{cwd.assets.frpc} reload -c {self._config_file}")

    def stop(self) -> None:
        if not self.alive: return

        with self.lock:
            if self.process is None: return
            self.process.terminate()
            self.process = None

    def log_add(self, content: str) -> None:
        while True:
            s = content.find("\033")
            if s == -1: break
            m = content[s:].find("m", s)
            if m == -1: break
            content = content[:s] + content[m+1:]

        with self.lock:
            self._logs.append(content)
            core.event.emit(INSTANCE_LOG_UPDATED)

    def log_pop(self) -> list[str]:
        with self.lock:
            logs = self._logs[self._log_index:]
            self._log_index = len(self._logs)
            return logs

    def log_index_clear(self) -> None:
        with self.lock:
            self._log_index = 0

    def _log_stdout(self) -> NoReturn:
        time.sleep(0.1)
        if self.process is None: raise SystemExit(0)
        if self.process.stdout is None: raise SystemExit(0)

        while self.alive:
            line = self.process.stdout.readline().decode("utf-8").strip()
            if line: self.log_add(line)

        core.event.emit(INSTANCE_SWITCHED)
        raise SystemExit(0)

    def _log_stderr(self) -> NoReturn:
        time.sleep(0.1)
        if self.process is None: raise SystemExit(0)
        if self.process.stderr is None: raise SystemExit(0)

        while self.alive:
            line = self.process.stderr.readline().decode("utf-8").strip()
            if line: self.log_add(line)

        raise SystemExit(0)

    def load_config(self) -> dict:
        try:
            with open(self._config_file, "rb") as f:
                return tomllib.load(f)

        except Exception:
            return {}

    def save_config(self, config: dict, update: bool = True) -> None:
        with open(self._config_file, "w", encoding="utf-8") as f:
            toml.dump(config, f)


def initialize_first() -> None:
    module.services = Services()


def initialize_final() -> None:
    module.services.load()
