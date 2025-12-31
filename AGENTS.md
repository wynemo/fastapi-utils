# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 使用语言

使用中文

## Project Overview

This is a Python library (`fastapi-toolbox`) that provides common utilities for working with FastAPI applications. The project is in early development stage with minimal structure currently in place.

## Development Environment

- **Package Manager**: uv (modern Python package and project manager)
- **Dependencies**: FastAPI and Starlette for web framework functionality

## Project Structure

- `__init__.py`: Package initialization, exports StaticFilesCache
- `static_files.py`: Static files utilities including StaticFilesCache class
- `main.py`: Entry point with basic hello world functionality
- `pyproject.toml`: Project configuration and metadata


## Publishing to PyPI

bash publish.sh
