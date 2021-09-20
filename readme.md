# LVMath

The internal website of the Lawrenceville Math Club.

# Development (Python 3.9)

## Notes

- Currently, when working with SQLAlchemy, use https://docs.sqlalchemy.org/en/14/tutorial/index.html.

### To Do

- Connect SQLAlchemy Column.default and WTForms Field.default in `model_form`.
- Add section to README explaining how to set up Google authentication in Google Cloud and then download the client secrets.

## Variables and Configuration

- The `DATABASE_URL` environment variable should point to the database (including SQL driver).
- The `sqlalchemy.url` variable in `alembic.ini` should be set to the value of `DATABASE_URL`.

## Database Migrations

To generate a revision, run the following command, where `NAME` is the name of the revision, such as "create user model". Take note of [the types of changes that alembic can detect](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).

```py -m alembic revision --autogenerate -m "NAME"```

To upgrade the database (after every fetch), run the following command.

```py -m alembic upgrade head```

## Environment Setup

### Windows

```
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

## Format (Before Commit)

### Windows

```
py -m black .
```
