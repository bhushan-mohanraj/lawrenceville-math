# LMC

The official website of the Lawrenceville Math Club.

# Development (Python 3.9)

## Environment

### macOS

```
python3 -m venv venv
source venv/bin/activate
```

### Windows

```
py -m venv venv
venv\Scripts\activate
```

## Dependencies

### macOS

```
python3 -m pip install -r requirements.txt
```

### Windows

```
py -m pip install -r requirements.txt
```

## Environment Variables

In production, the `SECRET_KEY` environment variable should be set to a secure key (generated, for example, with the `secrets` module). The `DATABASE_URL` environment variable can also be set.
