__all__ = [
    "__version__",
]

PACKAGE_NAME = "django-role"


from importlib.metadata import metadata


package_metadata = metadata(PACKAGE_NAME)
__version__ = package_metadata["Version"]