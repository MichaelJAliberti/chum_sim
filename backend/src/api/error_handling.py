from flask_restful import abort


def abort_if_does_not_exist(key, data):
    """throws a curl status error if a given key does not exist in a dictionary

    :param key: key into data
    :type key: str
    :param data: dictionary of api data
    :type data: dict
    """
    if id not in data:
        abort(404, message=f"Element {key} doesn't exist.")


def abort_if_operation_unsupported(operation, name):
    """throws a curl status error if a given operation cannot be applied to the calling
    resource

    :param operation: curl operation name
    :type operation: str
    :param name: url path to the calling resource
    :type name: str
    """
    abort(405, message=f"{operation.upper()} not supported for resource {name}.")
