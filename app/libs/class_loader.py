import importlib
import logging


def load_class(name: str):
    """
    load class by name
    """
    name_components = name.split(".")
    if not name_components:
        logging.error("Invalid class name: %s", name)
        return

    module_name = ".".join(name_components[:-1])
    class_name = name_components[-1]

    try:
        module = importlib.import_module(module_name)
        a_class = getattr(module, class_name)
        logging.info("load class: %s", a_class)
        return a_class
    except ImportError:
        logging.error("Module not found: %s", name)
    except AttributeError:
        logging.error("Class not found: %s", name)
