import inspect


def is_iterable(obj):
    return (
        hasattr(obj, "__iter__")
        and hasattr(obj, "__next__")
        and callable(obj.__iter__)
        and obj.__iter__() is obj
    )


def get_class_that_defined_method(meth):
    cls = getattr(
        inspect.getmodule(meth),
        meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
        None,
    )
    if isinstance(cls, type):
        return cls
