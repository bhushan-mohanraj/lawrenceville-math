# LMC

The internal website of the Lawrenceville Math Club.

# Development (Python 3.9)

## Notes

- Currently, when working with SQLAlchemy, use https://docs.sqlalchemy.org/en/14/tutorial/index.html.

### To Do

- Use Alembic for SQLAlchemy migrations.
- Add `setup.py` for deployment.
- Add Google authentication limited to `@lawrenceville.org` email addresses.

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

## Environment Variables

In production, the `SECRET_KEY` environment variable should be set to a secure key (generated, for example, with the `secrets` module). The `DATABASE_URL` environment variable can also be set.
