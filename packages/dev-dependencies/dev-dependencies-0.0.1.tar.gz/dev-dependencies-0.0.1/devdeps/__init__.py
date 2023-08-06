from importlib.metadata import PackageNotFoundError, version

VERSION: str | None = None
try:
    VERSION = version("dev-dependencies")
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
