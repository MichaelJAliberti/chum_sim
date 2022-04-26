def copy_class_def(*, name, class_def):
    """creates a new class definition that copies clas_def

    :param name: name for new class
    :type name: str
    :param class_def: the original class definition
    :type class_def: type

    :return: a copy of class_def with a new name
    :rtype: type
    """
    # source:
    # https://stackoverflow.com/questions/9363068/why-python-exec-define-class-not-working
    return type(name, (class_def,), {})
