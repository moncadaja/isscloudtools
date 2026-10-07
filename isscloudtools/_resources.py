"""Keep packaged resources available for Qt for the lifetime of the process."""

import atexit
from contextlib import ExitStack
from functools import cache
from importlib.resources import as_file, files

_resources = ExitStack()
atexit.register(_resources.close)


@cache
def resource_filename(name):
    """Return a filesystem path, extracting zipped resources when necessary."""
    return str(_resources.enter_context(as_file(files(__package__).joinpath(name))))