[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPI version](https://badge.fury.io/py/logging-basic-config.svg)](https://badge.fury.io/py/logging-basic-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/msantino.svg?style=social&label=Follow)](https://twitter.com/msantino)



# Basic Python Logging Configuration

This is a Python pip package that provides a simple function called `config()` that sets up the logging configuration for a Python project. 

## How it Works

The `config()` function takes in three optional arguments: `logging_level`, `libs_to_silence`, and `env_var_hide_timestamp`. 

- `logging_level` specifies the minimum logging level that should be recorded. The default value is "INFO". 
- `libs_to_silence` is a list of external libraries whose logging should be silenced. By default, several commonly used libraries are silenced. 
- `env_var_hide_timestamp` is an environment variable that can be set to hide the timestamp in the log messages.

The function then proceeds to set up the logging configuration based on the provided arguments. It first sets the logging level for external libraries to `logging.ERROR`. 

Next, it checks the `LOGGING_LEVEL` environment variable and uses its value if it is set, otherwise it uses the `logging_level` argument. 

The log format is then set depending on whether `env_var_hide_timestamp` is set or not. If it is set, the format only includes the log level, filename, and line number. Otherwise, the format includes the timestamp, log level, filename, and line number. 

Finally, the function creates a `StreamHandler` that logs to the standard output, sets the formatter to the log format, adds the handler to the logger, and sets the logging level to the specified level. 

The logger is then returned so that it can be used throughout the project to log messages at the specified level.

Overall, `logging_basic_config` simplifies the process of configuring logging in a Python project, making it easier to customize the logging level and format, and to silence external libraries.

## Example

### Install package

```bash
pip install logging-basic-config
```

### Using the library

```python
import logging_basic_config

logging = logging_basic_config.config(logging_level="DEBUG")

logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```

### In additional files

Once the `logging_basic_config.config(logging_level="DEBUG")` code was called in your `main` or entrypoint call, you only need to import `logging` and use it in other files. 

```python:anotherfile.py
import logging

logging.info("This is another info message")
```