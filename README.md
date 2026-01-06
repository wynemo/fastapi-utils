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

Or install directly from GitHub:

```bash
uv add git+https://github.com/wynemo/fastapi-utils.git
```

```bash
pip install git+https://github.com/wynemo/fastapi-utils.git
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
        filter_callbacks=[filter_sqlalchemy],
        reload=True  # Enable hot reload (development only)
    )
```


#### Hot Reload Mode

The `reload` parameter enables automatic server restart when code changes are detected. This is useful during development:

```python
run_server(
    "main:app",
    host="127.0.0.1",
    port=8000,
    reload=True,  # Enable hot reload
    reload_dirs=["src"],  # Optional: specify directories to watch
)
```

**Note**:
- Hot reload mode uses `fork` internally, which differs from multi-process mode (`workers >= 2`) that uses `spawn`
- File logging behaves differently in reload mode to avoid multiple processes writing to the same file
- **Do not use `reload=True` in production**

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

### NextJSRouteMiddleware

`NextJSRouteMiddleware` is a middleware for handling Next.js static export routes. When a request returns 404, it attempts to find the corresponding `.html` file.

#### Basic Usage

```python
from fastapi import FastAPI
from fastapi_toolbox import NextJSRouteMiddleware

app = FastAPI()

# Add middleware
app.add_middleware(
    NextJSRouteMiddleware,
    static_dir="frontend/dist",
    skip_prefixes=["/api", "/static", "/docs", "/openapi.json", "/redoc"],
)
```

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `static_dir` | Static files directory path | Required |
| `skip_prefixes` | List of path prefixes to skip processing | `[]` |
| `index_file` | Default filename for root path (without extension) | `"index"` |

#### How It Works

1. Requests matching `skip_prefixes` are passed through directly
2. Other requests are processed normally
3. If 404 is returned and path doesn't start with `/_next`, it looks for the corresponding `.html` file
4. For example: `/about` → looks for `frontend/dist/about.html`
5. Root path `/` → looks for `frontend/dist/index.html`

#### Practical Example

```python
from fastapi import FastAPI
from fastapi_toolbox import NextJSRouteMiddleware, StaticFilesCache
import os

app = FastAPI()

front_folder = os.path.join(os.path.dirname(__file__), "frontend/dist")

# Add Next.js route middleware
app.add_middleware(
    NextJSRouteMiddleware,
    static_dir=front_folder,
    skip_prefixes=[
        "/api",
        "/static",
        "/_next",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/favicon.ico",
    ],
)

# Mount static files
app.mount("/", StaticFilesCache(directory=front_folder), name="static")
```

### Settings

`Settings` is a configuration class based on pydantic-settings that supports loading configuration from environment variables or `.env` files.

#### Basic Usage

```python
from fastapi_toolbox import Settings, settings

# Use the default settings instance (automatically loads from environment variables or .env)
print(settings.DATABASE_URL)

# Or create a custom Settings class
class MySettings(Settings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/mydb"
    API_KEY: str = "default-key"

my_settings = MySettings()
```

#### Key Features

- **Environment Variable Support**: Automatically loads from environment variables
- **.env File Support**: Automatically reads `.env` files
- **Inheritance Friendly**: Easily extend with custom configuration fields
- **Type Safe**: Full Pydantic validation and type checking

### Database

`fastapi-toolbox` provides a set of database utilities based on SQLModel, making it easy to integrate databases into your FastAPI application.

#### Basic Usage

```python
from fastapi import FastAPI, Depends
from fastapi_toolbox import init_database, get_session, create_db_and_tables
from sqlmodel import Session, SQLModel, Field

app = FastAPI()

# Define your models
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_database(database_url="sqlite:///./test.db")
    create_db_and_tables()

# Use dependency injection to get database sessions
@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

#### Configuration Methods

`init_database` supports three configuration methods (in order of priority):

```python
from fastapi_toolbox import Settings, init_database

# Method 1: Pass database_url directly
init_database(
    database_url="postgresql://user:pass@localhost:5432/mydb",
    echo=True,  # Enable SQL logging
    pool_size=10
)

# Method 2: Use custom Settings instance
class MySettings(Settings):
    DATABASE_URL: str = "postgresql://user:pass@prod:5432/prod_db"

my_settings = MySettings()
init_database(settings_instance=my_settings)

# Method 3: Use default settings (reads from .env or environment variables)
# Set DATABASE_URL in .env or environment
init_database()
```

#### Available Functions

| Function | Description |
|----------|-------------|
| `init_database()` | Initialize database engine with flexible configuration options |
| `get_engine()` | Get the database engine instance (auto-initializes if needed) |
| `get_session()` | Dependency injection function for database sessions |
| `create_db_and_tables()` | Create all tables based on SQLModel models |

## Build

uv build

## Publish

uv publish

Enter `__token__` as username and then enter your PyPI token

## License

MIT
