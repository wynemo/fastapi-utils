# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library (`fastapi-utils`) that provides common utilities for working with FastAPI applications. The project is in early development stage with minimal structure currently in place.

## Development Environment

- **Python Version**: 3.12 (specified in `.python-version`)
- **Package Manager**: uv (modern Python package and project manager)
- **Dependencies**: Currently no external dependencies defined

## Project Structure

- `main.py`: Entry point with basic hello world functionality
- `pyproject.toml`: Project configuration and metadata
- `.python-version`: Specifies Python 3.12 requirement

## Common Commands

- **Install dependencies**: `uv sync`
- **Add new dependency**: `uv add <package-name>`
- **Add development dependency**: `uv add --dev <package-name>`
- **Run the main module**: `uv run python main.py`
- **Install in development mode**: `uv pip install -e .`
- **Create virtual environment**: `uv venv`

## Notes

- The project is currently a minimal skeleton
- No testing framework, linting tools, or CI/CD configured yet
- Future development will likely involve adding FastAPI-specific utilities and dependencies