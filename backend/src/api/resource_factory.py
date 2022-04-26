from flask_restful import reqparse, Resource

from src.api.error_handling import (
    abort_if_does_not_exist,
    abort_if_operation_unsupported,
)
from src.api.utils import copy_class_def


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, template_data, required_fields=[]):
        """generates resources based on template_data and returns them

        :param template_data: data to convert into resources
        :type template_data: dict
        :param required_fields: fields required for POST requests
        :type required_fields: dict

        :return: list of dictionaries of resource classes and urls
        :rtype: list
        """
        data = _copy_keys_from_template(template_data)
        resources = []
        make_resources_per_layer(
            template_data=template_data,
            data=data,
            resources=resources,
            required_fields=required_fields,
        )

        return resources


def make_resources_per_layer(
    *, template_data, data, resources, key_chain=[], required_fields=[]
):
    """recursively generates resources by parsing template_data and appends them
    to resources

    :param template_data: data to convert into resources
    :type template_data: dict
    :param data: full data dictonary for the api
    :type data: dict
    :param resources: list of resources to append to
    :type resources: list
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param required_fields: fields required for POST requests
    :type required_fields: dict
    """
    if isinstance(template_data, dict):
        make_dict_layer_resource(
            template_data=template_data,
            data=data,
            resources=resources,
            key_chain=key_chain,
            required_fields=required_fields,
        )
    elif isinstance(template_data, list):
        make_list_layer_resource(
            template_data=template_data,
            data=data,
            resources=resources,
            key_chain=key_chain,
            required_fields=required_fields,
        )


def make_list_layer_resource(
    *, template_data, data, resources, key_chain, required_fields
):
    """generates resource for a list layer in template_data, then calls
    make_resources_per_layer to continue generating resources

    :param template_data: data to convert into a resource
    :type template_data: list
    :param data: full data dictonary for the api
    :type data: dict
    :param resources: list of resources to append to
    :type resources: list
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param required_fields: fields required for POST requests
    :type required_fields: dict
    """
    if not isinstance(template_data, list):
        return

    url = _get_url(key_chain)

    parser = _get_parser(template_data=template_data, required_fields=required_fields)

    new_resource = _make_list_resource(
        data=data,
        key_chain=key_chain,
        url=url,
        put_parser=parser,
        post_parser=parser,
    )

    resources.append({"class": new_resource, "url": url})


def make_dict_layer_resource(
    *, template_data, data, resources, key_chain, required_fields
):
    """generates resource for a dictionary layer in template_data, then calls
    make_resources_per_layer to continue generating resources

    :param template_data: data to convert into resources
    :type template_data: dict
    :param data: full data dictonary
    :type data: dict
    :param resources: list of resources to append to
    :type resources: list
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param required_fields: fields required for POST requests
    :type required_fields: dict
    """
    if not isinstance(template_data, dict):
        return

    for key, value in template_data.items():
        local_chain = key_chain.copy()
        local_chain.append(key)
        url = _get_url(local_chain)

        if isinstance(value, dict):
            parser = _get_parser(
                template_data=_get_value_ref(value), required_fields=required_fields
            )
            if "<id>" in list(value.keys()):
                # make each branch its own dictionary?
                new_resource = _make_outer_dict_resource(
                    data=data[key],
                    key_chain=local_chain,
                    url=url,
                    post_parser=parser,
                )
            else:
                new_resource = _make_inner_dict_resource(
                    data=data, key_chain=local_chain, url=url, put_parser=parser
                )
            resources.append({"class": new_resource, "url": url})

        make_resources_per_layer(
            template_data=value,
            data=data,
            resources=resources,
            key_chain=local_chain,
        )


def _copy_keys_from_template(template_data):
    """copies top-level keys and types from a template into a new dictionary

    :param template_data: partial of full api template data dictionary
    :type template_data: dict

    :return: a new dictionary
    :rtype: dict
    """
    data = {}
    for key, value in template_data.items():
        data[key] = (
            {} if isinstance(value, dict) else [] if isinstance(value, list) else None
        )

    return data


def _get_url(key_chain):
    """creates an appropriate resource url from keys traversed in the template

    :param key_chain: list of keys traversed so far
    :type key_chain: list

    :return: a resource url
    :rtype: str
    """
    return "/" + "/".join(key_chain)


def _get_value_ref(value):
    """returns a value reference in a dictionary, attempts to parse
    past key words like "<id>"

    :param value: value at some key in a dictionary
    :type value: any

    :return: a reference to a value in a dictionary
    :rtype: any
    """
    value_ref = value
    if isinstance(value, dict) and list(value.keys())[0] == "<id>":
        value_ref = value["<id>"]

    return value_ref


def _get_parser(*, template_data, required_fields=[]):
    """get parser for PUT or POST operation

    :param template_data: partial api template data dictionary
    :type template_data: dict
    :parm required_fields: a list of fields required for post operations
    :type required_fields: list

    :return: a parser for PUT or POST requests
    :rtype: reqparse.RequestParser
    """
    parser = reqparse.RequestParser()

    if isinstance(template_data, list):
        if template_data:
            parser.add_argument(
                "value",
                type=type(template_data[0]),
            )
    elif isinstance(template_data, dict):
        for field, value in template_data.items():
            parser.add_argument(
                field,
                type=type(value),
                required=True if field in required_fields else False,
            )

    return parser


def _make_list_resource(*, data, key_chain, url, put_parser, post_parser):
    """INCOMPLETE FUNCTION
    creates restful resource based on a list element in the template

    :param data: dictonary of data for the api
    :type data: dict
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param url: path to the resulting resource
    :type url: str
    :param put_parser: parser for the payload of a PUT request
    :type put_parser: reqparse.RequestParser
    :param post_parser: parser for the payload of a POST request
    :type post_parser: reqparse.RequestParser

    :return: class definition for the generated resource
    :rtype: type
    """

    class ListResource(Resource):
        def get(self, **kwargs):
            id = kwargs["id"]
            return _traverse_key_chain(id=id, key_chain=key_chain, data=data)

        def delete(self, **kwargs):
            """clear the list"""
            # id = kwargs["id"]
            # local_data = _traverse_key_chain(
            #     id=id, key_chain=key_chain[:-1], data=data
            # )
            # key = id if key_chain[-1] == "<id>" else key_chain[-1]
            # abort_if_does_not_exist(key, local_data)

            # del local_data[key]
            return "", 204

        def put(self, **kwargs):
            """append to list"""
            id = kwargs["id"]
            local_data = _traverse_key_chain(id=id, key_chain=key_chain, data=data)
            # args = put_parser.parse_args()
            # for field in args.keys():
            #     if args[field]:
            #         local_data[field] = args[field]
            return local_data, 201

        def post(self, **kwargs):
            abort_if_operation_unsupported("POST", url)

    return copy_class_def(name=url, class_def=ListResource)


def _make_outer_dict_resource(*, data, key_chain, url, post_parser):
    """creates restful resource based on an intter dictionary element in the template

    :param data: dictonary of data for the api
    :type data: dict
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param url: path to the resulting resource
    :type url: str
    :param post_parser: parser for the payload of a POST request
    :type post_parser: reqparse.RequestParser

    :return: class definition for the generated resource
    :rtype: type
    """

    class OuterResource(Resource):
        def get(self):
            return data

        def delete(self):
            abort_if_operation_unsupported("DELETE", url)

        def put(self):
            abort_if_operation_unsupported("PUT", url)

        def post(self):
            args = post_parser.parse_args()
            id = str(int(max(data.keys())) + 1 if data.keys() else 1)
            data[id] = {}  # f"{url}<id>": id
            for field in args.keys():
                data[id][field] = args[field]
            return {id: data[id]}, 201

    return copy_class_def(name=url, class_def=OuterResource)


def _make_inner_dict_resource(*, data, key_chain, url, put_parser):
    """creates restful resource based on outermost dictionary element in the template

    :param data: dictonary of data for the api
    :type data: dict
    :param key_chain: chain of keys so far to form url path for resource
    :type key_chain: list
    :param url: path to the resulting resource
    :type url: str
    :param put_parser: parser for the payload of a PUT request
    :type put_parser: reqparse.RequestParser

    :return: class definition for the generated resource
    :rtype: type
    """

    class InnerResource(Resource):
        def get(self, **kwargs):
            id = kwargs["id"]
            return _traverse_key_chain(id=id, key_chain=key_chain, data=data)

        def delete(self, **kwargs):
            id = kwargs["id"]
            local_data = _traverse_key_chain(id=id, key_chain=key_chain[:-1], data=data)
            key = id if key_chain[-1] == "<id>" else key_chain[-1]
            abort_if_does_not_exist(key, local_data)

            del local_data[key]
            return "", 204

        def put(self, **kwargs):
            id = kwargs["id"]
            local_data = _traverse_key_chain(id=id, key_chain=key_chain, data=data)

            # temporary fix until above post generates nested lists
            if not isinstance(local_data, dict):
                layer_above = _traverse_key_chain(
                    id=id, key_chain=key_chain[:-1], data=data
                )
                layer_above[key_chain[-1]] = {}
                local_data = layer_above[key_chain[-1]]

            args = put_parser.parse_args()
            for field in args.keys():
                if args[field]:
                    local_data[field] = args[field]
            return local_data, 201

        def post(self, **kwargs):
            abort_if_operation_unsupported("POST", url)

    return copy_class_def(name=url, class_def=InnerResource)


def _traverse_key_chain(*, id, key_chain, data):
    """index into data along keys in key chain

    :param id: numerical identifier within data
    :type id: str
    :param key_chain: chain of keys to be traversed
    :type key_chain: list
    :param data: data for the api
    :type param: dict

    :return: the value in data at the end of key_chain
    :rtype: any
    """
    local_data = data
    for key in key_chain:
        if key == "<id>":
            abort_if_does_not_exist(id, local_data)
            local_data = local_data[id]
        else:
            abort_if_does_not_exist(key, local_data)
            local_data = local_data[key]

    return local_data
