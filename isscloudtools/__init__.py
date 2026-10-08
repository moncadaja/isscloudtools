"""Cloud service integrations for the ISS beamline."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("isscloudtools")
except PackageNotFoundError:
    __version__ = "0+unknown"
