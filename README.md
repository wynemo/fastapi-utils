# FastAPI Toolbox

[中文文档](README.zh.md) | English

A Python library that provides common utilities and features for FastAPI development, including static file cache control and advanced logging system.

## Installation

```bash
uv add fastapi-toolbox
```

```bash
pip install fastapi-toolbox
```

## Features

### Running Server

`fastapi-toolbox` provides an advanced logging system based on loguru, supporting log configuration in multi-process environments.

#### Basic Usage

```python
from fastapi import FastAPI
from fastapi_toolbox import logger, run_server
import uvicorn
import logging

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Hello World accessed")
    return {"Hello": "World"}

if __name__ == "__main__":

    def filter_sqlalchemy(record):
        if record.name.startswith("sqlalchemy"):
            if record.levelno < logging.ERROR:
                return True

    run_server(
        "main:app",
        host="127.0.0.1",
        port=8000,
        workers=1,
        log_file="logs/app.log", # Log rotation
        filter_callbacks=[filter_sqlalchemy]
    )
```


#### Environment Variable Configuration

- `LOG_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR), defaults to INFO
- `JSON_LOGS`: Set to "1" to enable JSON format logs, defaults to standard format

#### Key Features

- **Multi-process Support**: `UvicornConfig` ensures logs work properly in multi-process environments
- **Auto Rotation**: Supports log rotation by file size and time
- **Unified Interception**: Automatically intercepts standard library logging and forwards to loguru
- **Flexible Configuration**: Supports environment variables and code configuration

### StaticFilesCache

`StaticFilesCache` is an enhanced version of FastAPI StaticFiles, providing configurable cache control for static files.

#### Basic Usage

```python
from fastapi import FastAPI
from fastapi_toolbox import StaticFilesCache
import os

app = FastAPI()

# Example 1: Using default cache policy (cache disabled)
front_folder = os.path.join(os.path.dirname(__file__), "frontend/dist")
app.mount("/", StaticFilesCache(directory=front_folder), name="static")

# Example 2: Using custom cache policy
app.mount("/static", StaticFilesCache(
    directory="static_files",
    cachecontrol="max-age=3600"  # Cache for 1 hour
), name="static")
```

#### Key Features

- **Auto Cache Control**: Automatically adds Cache-Control response headers for `.html` and `.txt` files
- **Configurable Policy**: Customize cache behavior via `cachecontrol` parameter
- **Full Compatibility**: Inherits from FastAPI StaticFiles, retaining all original functionality

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `directory` | Static files directory path | Required |
| `cachecontrol` | Cache-Control header value | `"no-cache, no-store, must-revalidate"` |
| Other parameters | Same as standard StaticFiles | - |

#### Common Cache Strategies

```python
# Disable cache (suitable for development)
cachecontrol="no-cache, no-store, must-revalidate"

# Short-term cache (suitable for frequently updated resources)
cachecontrol="max-age=3600"  # 1 hour

# Long-term cache (suitable for rarely changed resources)
cachecontrol="public, max-age=86400"  # 1 day

# Private cache, must revalidate
cachecontrol="private, must-revalidate"
```

#### Practical Use Cases

Suitable for scenarios where you need to serve static files for frontend SPA applications:

```python
# Access http://127.0.0.1:8000/index.html to view the frontend page
front_folder = os.path.join(os.path.dirname(__file__), "frontend/dist")
app.mount("/", StaticFilesCache(directory=front_folder), name="static")
```

With this configuration, HTML files will not be cached by the browser, ensuring users always get the latest version of the frontend application.

## Build

uv build

## Publish

uv publish

Enter `__token__` as username and then enter your PyPI token

## License

MIT
