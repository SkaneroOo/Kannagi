from enum import Enum
from datetime import datetime as dt

class LogLevel(Enum):
    DEBUG = 31
    INFO = 15
    WARN = 7
    ERROR = 3
    CRITICAL = 1
    DISABLED = 0

class Logger:

    def __init__(self, name: str, log_level: LogLevel = LogLevel.DEBUG):
        self.name = name
        self.log_level = log_level

    def set_log_level(self, log_level: LogLevel):
        self.log_level = log_level

    def debug(self, message):
        if self.log_level.value & 0b10000:
            print(f"\033[90m{dt.now().strftime('%Y-%m-%d %H:%M:%S')} \033[90m{'DEBUG':<8} \033[95m{self.name} \033[0m{message}")

    def info(self, message):
        if self.log_level.value & 0b1000:
            print(f"\033[90m{dt.now().strftime('%Y-%m-%d %H:%M:%S')} \033[94m{'INFO':<8} \033[95m{self.name} \033[0m{message}")

    def warn(self, message):
        if self.log_level.value & 0b100:
            print(f"\033[90m{dt.now().strftime('%Y-%m-%d %H:%M:%S')} \033[93m{'WARN':<8} \033[95m{self.name} \033[0m{message}")

    def error(self, message):
        if self.log_level.value & 0b10:
            print(f"\033[90m{dt.now().strftime('%Y-%m-%d %H:%M:%S')} \033[91m{'ERROR':<8} \033[95m{self.name} \033[0m{message}")

    def critical(self, message):
        if self.log_level.value & 0b1:
            print(f"\033[90m{dt.now().strftime('%Y-%m-%d %H:%M:%S')} \033[91m{'CRITICAL':<8} \033[95m{self.name} \033[91m{message}")