import logging
import datetime
import os

class Setup_Logger(object):
    def __init__(self):
        """
        https://realpython.com/python-logging/
        If the logger's log_level is higher than its handlers, than the handlers messages will not be logged.
        In otherwords, Handlers can’t show logs lower than the defined log level of the logger they’re connected to.
        """
        self.suffix = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # for keeping the filename common
        if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
            os.mkdir(os.path.join(os.getcwd(), "logs"))
        self.setup_logger("WARNING", "DEBUG")

    def setup_logger(self, console_level, file_level):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(10)
        formatter = logging.Formatter("{asctime}:{msecs:03.0f}  -  {levelname:8s}  -  {message}",
                                      style="{",
                                      datefmt="%Y-%m-%d %H:%M:%S", )  # Common Formatter for both Console and Filehandler
        # send logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # write logs to your file
        file_handler = logging.FileHandler(f"./logs/{self.suffix}.log", mode="a", encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

if __name__ == "__main__":
    a = Setup_Logger()