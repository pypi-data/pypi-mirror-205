# -*- coding: utf-8 -*-
import binascii
import os
import sys
import time

from typing import Optional

from coppyr.lazyproperty import lazyproperty
from coppyr.collections import cycle, DotDict
from coppyr.singleton import Singleton, Namespace


# TODO: These sys variables should really be applied elsewhere.
sys.tracebacklimit = 10000
sys.setrecursionlimit(2048)


class TimeKeeper:
    def __init__(self):
        self.timings = []
        self.relative_base = time.time()

    def checkpoint(self, name=None):
        name = name if name is not None else Context().action_id
        now = time.time()
        self.timings.append(
            (name, now, now - self.relative_base, Context().action_duration)
        )

    @property
    def profile(self):
        profile = {}

        for _, timing in enumerate(self.timings):
            name, stamp, relative, duration = timing
            profile[name] = (stamp, f"{relative:.3f}s", f"{duration:.3f}s")

        return profile


class Context(Singleton):
    """
    A simple interpreter local context that can be used as a shared memory
    space without relying on "global" or careful variable passing.
    """
    def __init__(
        self,
        app_name: Optional[str]=None,
        config_path: Optional[str]=None,
        reinitialize: bool=False
    ):
        # skip duplicate initialization calls
        if not self._init and not reinitialize:
            return

        # constant vars
        self.app_name = app_name if app_name is not None else "piston"
        self.pid = os.getpid()
        self.config_path = config_path

        # dynamic vars
        self.ids = cycle(100000, 1000000)
        self.action_id = f"{self.pid}_{next(self.ids)}"
        self.action_stamp = time.time()
        self.logging_keys = [
            "action_id",
            "action_duration",
            "action_duration_str"
        ]

        # utility namespace
        self.namespace = Namespace()

        super().__init__()

    def setup(self):
        """
        Helper method that ensure some order dependent things are lazy loaded
        in the correct order.
        """
        self.config
        self.log

    @lazyproperty
    def app_name_env(self):
        return self.app_name.replace("-", "_")\
                            .replace(".", "__")\
                            .upper()

    @lazyproperty
    def ident(self):
        random_hex = binascii.b2a_hex(os.urandom(4)).decode()
        return random_hex

    @lazyproperty
    def cwd(self):
        return os.getcwd()

    def inc_action_id(self):
        self.action_id = f"{self.pid}_{next(self.ids)}"  # increment action_id
        self.action_stamp = time.time()  # reset start time for new action

    @property
    def action_duration(self):
        return time.time() - self.action_stamp

    @property
    def action_duration_str(self):
        return f"{self.action_duration:.3f}"

    @lazyproperty
    def hostname(self):
        import socket
        return socket.gethostname()

    @lazyproperty
    def fqdn(self):
        import socket
        return socket.getfqdn()

    @lazyproperty
    def config(self):
        if self.config_path:
            from coppyr.config import YAMLConfig
            return YAMLConfig(self.config_path)
        else:
            return DotDict()

    @lazyproperty
    def log(self):
        from coppyr import logger

        if self.config.get("LOG_SETUP", True):
            logger.setup()

        if self.config.LOG_DISABLED:
            return logger.get("devnull")
        elif self.config.LOG_STDOUT:
            return logger.get("stdout", level=self.config.LOG_LEVEL)
        else:
            return logger.get(level=self.config.LOG_LEVEL)

    def get_file_handlers(self):
        # This helper is used by python-daemon to preserve file handlers when
        # starting a daemonized process.
        fds = [
            self.log.handlers[0].stream  # log file handler
        ]

        return fds

    @lazyproperty
    def timer(self):
        return TimeKeeper()
