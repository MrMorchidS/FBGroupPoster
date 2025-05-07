import logging


class Logger:
    def __init__(self, log_dir="log"):
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        # Create handlers
        self.stdout_handler = logging.FileHandler(f"{log_dir}/out.log")
        self.stderr_handler = logging.FileHandler(f"{log_dir}/err.log")

        # Set handler levels
        self.stdout_handler.setLevel(logging.INFO)
        self.stderr_handler.setLevel(logging.ERROR)

        # Add filters to handlers
        # stdout_handler only allows INFO and WARNING
        self.stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        # stderr_handler allows ERROR and above (filter is redundant here but explicit)
        self.stderr_handler.addFilter(lambda record: record.levelno >= logging.ERROR)

        # Apply formatter
        formatter = logging.Formatter(log_format, datefmt=date_format)
        self.stdout_handler.setFormatter(formatter)
        self.stderr_handler.setFormatter(formatter)

        # Configure the logger
        self.logger = logging.getLogger("customLogger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.stdout_handler)
        self.logger.addHandler(self.stderr_handler)
        self.logger.propagate = False

    def __getattr__(self, attr):
        return getattr(self.logger, attr)
