import os
import logging
from logging.handlers import RotatingFileHandler
import atexit

class Logger:
    _logger = None

    @staticmethod
    def get_logger(path, level=logging.DEBUG, max_log_size=10*1024*1024, backup_count=3):
        if Logger._logger is None:
            Logger._logger = logging.getLogger(__name__)
            Logger._logger.setLevel(level)
            if not Logger._logger.handlers:
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(formatter)

                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                    except Exception as e:
                        print(f"Error creating log directory: {e}")
                        path = './'  # Default to current directory if there's an error

                log_file_path = os.path.join(path, 'application.log')
                file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)

                Logger._logger.addHandler(console_handler)
                Logger._logger.addHandler(file_handler)

                # Register the close_handlers method to be called upon program exit
                atexit.register(Logger.close_handlers)
        
        return Logger._logger

    @staticmethod
    def close_handlers():
        if Logger._logger:
            for handler in Logger._logger.handlers:
                handler.close()
                Logger._logger.removeHandler(handler)
