import logging
import colorama
import sys
try:
    from src.config import LOG_LEVEL, LOG_FILENAME, LOG_SHOW_DATE
except ImportError as e:
    LOG_LEVEL = logging.DEBUG
    LOG_FILENAME = None
    LOG_SHOW_DATE = False

colorama.init()

# Определяем уровни TRACE и SUCCESS
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

LOG_LEVEL_MAP = {
    "TRACE": TRACE_LEVEL,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "SUCCESS": SUCCESS_LEVEL,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

if LOG_LEVEL in LOG_LEVEL_MAP:
    LOG_LEVEL = LOG_LEVEL_MAP[LOG_LEVEL]

class CustomLogger(logging.Logger):
    def trace(self, message: str, *args, **kwargs) -> None:
        if self.isEnabledFor(TRACE_LEVEL):
            self._log(TRACE_LEVEL, message, args, **kwargs)

    def success(self, message: str, *args, **kwargs) -> None:
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.setLoggerClass(CustomLogger)

class CustomFormatter(logging.Formatter):
    prefix_date = " : %Y-%m-%d" if LOG_SHOW_DATE else ""
    prefix = f"[%(levelname)s : %(name)s%(asctime)s]"
    format = " %(message)s"

    FORMATS = {
        TRACE_LEVEL: colorama.Fore.CYAN + prefix + colorama.Style.RESET_ALL + format,
        logging.DEBUG: colorama.Fore.MAGENTA + prefix + colorama.Style.RESET_ALL + format,
        logging.INFO: colorama.Fore.BLUE + prefix + colorama.Style.RESET_ALL + format,
        SUCCESS_LEVEL: colorama.Fore.GREEN + prefix + colorama.Style.RESET_ALL + format,
        logging.WARNING: colorama.Fore.YELLOW + prefix + colorama.Style.RESET_ALL + format,
        logging.ERROR: colorama.Fore.RED + prefix + colorama.Style.RESET_ALL + format,
        logging.CRITICAL: colorama.Back.RED + prefix + colorama.Style.RESET_ALL + format
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=f"{self.prefix_date} : %H:%M:%S")
        return formatter.format(record)

def get_logger(name: str = "root", log_level: int = LOG_LEVEL) -> CustomLogger:
    log = logging.getLogger(name)
    log.propagate = False
    log.setLevel(log_level)

    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(CustomFormatter())
    log.addHandler(stdout)

    if LOG_FILENAME is not None:
        file_handler = logging.FileHandler(LOG_FILENAME)
        file_handler.setFormatter(CustomFormatter())
        log.addHandler(file_handler)

    return log