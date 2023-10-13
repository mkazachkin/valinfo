import logging
import os


class ViLogger:
    IS_ACTION: bool = True
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL

    def __init__(self, log_file_name: str, total_actions: int = 0, log_level: int = logging.DEBUG) -> None:
        hdlr = logging.FileHandler(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), log_file_name), mode='w')
        hdlr.setFormatter(logging.Formatter(
            "%(levelname)s [%(asctime)s] %(message)s"))
        self._logger = logging.getLogger(log_file_name)
        self._logger.setLevel(log_level)
        self._logger.addHandler(hdlr)
        self._total_actions: int = total_actions
        self._current_action: int = 0

    def print_log(self, message: str, level: int = INFO, is_action: bool = not IS_ACTION) -> None:
        if is_action:
            self._current_action += 1
            if self._current_action <= self._total_actions:
                self._logger.debug(int(self._current_action /
                                       self._total_actions * 100))
        if level == self.INFO:
            self._logger.info(message)
        elif level == self.WARNING:
            self._logger.warning(message)
        elif level == self.ERROR:
            self._logger.error(message)
        else:
            self._logger.critical(message)

    def set_total_actions(self, total_actions: int) -> None:
        self._total_actions = total_actions

    def get_total_actions(self) -> int:
        return self._total_actions

    def set_current_action(self, current_action: int) -> None:
        self._current_action = current_action

    def get_current_action(self) -> int:
        return self._current_action
