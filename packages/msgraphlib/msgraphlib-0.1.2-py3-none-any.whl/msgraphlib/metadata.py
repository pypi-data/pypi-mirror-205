### METADATA ###

from importlib.metadata import version 

class Metadata():
    PACKAGE_NAME = __name__.split('.')[0]
    PACKAGE_VERSION = version(PACKAGE_NAME)

    @classmethod
    def __init__(cls, caller):
        cls.MODULE_NAME = caller.__class__.__module__
        cls.CLASS_NAME = caller.__class__.__name__