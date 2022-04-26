from src.api.restful_service import RESTService
from template import DATA_TEMPLATE


service = RESTService.build_from_templates(DATA_TEMPLATE)
app = service.app


if __name__ == "__main__":
    app.run()
