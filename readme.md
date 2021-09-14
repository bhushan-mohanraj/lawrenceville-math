# LMC

The internal website of the Lawrenceville Math Club.

# Development (Python 3.9)

## Notes

- Currently, when working with SQLAlchemy, use https://docs.sqlalchemy.org/en/14/tutorial/index.html.

### To Do

- Use absolute imports (i.e. `from app import models`) rather than relative imports (i.e. `from .. import models`).
- Create single import file for models (i.e. `from . import Model, Column, String`).
- Add base `Form` class with CSRF.
- Add class-based CreateView, UpdateView, DeleteView, and CRUDView for DRY.

## Environment Setup

### macOS

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Windows

```
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

## Format (Before Commit)

### macOS

```
python3 -m black .
```

### Windows

```
py -m black .
```

### VSCode


In VSCode, with the Python extension installed, you can add the following settings to `settings.json`.

```
{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
}
```

## Environment Variables

In production, the `SECRET_KEY` environment variable should be set to a secure key (generated, for example, with the `secrets` module). The `DATABASE_URL` environment variable can also be set.
