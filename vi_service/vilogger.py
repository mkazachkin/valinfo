import logging
import os


class ViLogger:
    IS_ACTION: bool = True
    INFO: int = 1
    WARNING: int = 2
    ERROR: int = 3
    CRITICAL: int = 4

    def __init__(self, log_file_name: str, total_actions: int = 0) -> None:
        logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                       log_file_name), filemode='w')
        self._total_actions: int = total_actions
        self._current_action: int = 0

    def print_log(self, message: str, level: int = INFO, is_action: bool = not IS_ACTION) -> None:
        if is_action:
            self._current_action += 1
            if self._current_action <= self._total_actions:
                logging.debug(int(self._current_action /
                              self._total_actions * 100))
        if level == self.INFO:
            logging.info(message)
        elif level == self.WARNING:
            logging.warning(message)
        elif level == self.ERROR:
            logging.error(message)
        else:
            logging.critical(message)

    def set_total_actions(self, total_actions: int) -> None:
        self._total_actions = total_actions

    def get_total_actions(self) -> int:
        return self._total_actions

    def set_current_action(self, current_action: int) -> None:
        self._current_action = current_action

    def get_current_action(self) -> int:
        return self._current_action
