from flask import Flask
from flask_restful import Api

from src.api.resource_factory import ResourceFactory


class RESTService:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    @classmethod
    def build_from_templates(cls, *args):
        service = RESTService()
        for template in args:
            service._add_resources(
                ResourceFactory.make_resources(template_data=template)
            )
        return service

    @classmethod
    def build_from_resources(cls, *args):
        service = RESTService()
        [service._add_resources(resources) for resources in args]
        return service

    def _add_resources(self, resources):
        [
            self.api.add_resource(resource["class"], resource["url"])
            for resource in resources
        ]
