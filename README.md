## EchoCues API

Backend service and API for EchoCues.

## Running

The EchoCues API requires at least Python 3.9.
All dependencies are managed by Python `poetry`, which must be installed beforehand.

To install all packages required, run:
```sh
poetry install
```

> Please note, that if you run the following commands in an integrated terminal that automatically activates the virtual environment, or already know that you have the virtual environment activated, then you can omit the `poetry run` prefix, and just run the shell script as-is.

### Starting a development server:
```sh
poetry run sh debug.sh
```

