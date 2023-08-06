import importlib
from typing import Any


class ImportHelper:
    @classmethod
    def import_module(cls, module_name: str, *args) -> Any:
        module = importlib.import_module(module_name)
        if len(args) == 0:
            return module
        if len(args) == 1:
            return getattr(module, args[0])
        return [getattr(module, package_name) for package_name in args]
