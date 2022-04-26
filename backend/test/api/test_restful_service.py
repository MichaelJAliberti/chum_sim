import pytest

from src.data_management.restful_service import RESTService
from src.data_management.template import DATA_TEMPLATE


@pytest.fixture(scope="module", autouse=True)
def app():
    app = RESTService.build_from_templates(DATA_TEMPLATE).app
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture(scope="module", autouse=True)
def client(app):
    return app.test_client()


def perform_curl_op(client, operation, path, param):
    """Perfroms requested curl operation on resource indicated by path"""
    if operation == "GET":
        return client.get(path)
    elif operation == "POST":
        return client.post(path, json=param)
    elif operation == "PUT":
        return client.put(path, json=param)
    else:
        return client.delete(path)


@pytest.mark.parametrize(
    "operation, param, path, expected_code, expected_response",
    [
        # Outer Dictionary operation tests
        [
            "GET",
            "/chats",
            None,
            200,
            {},
        ],
        [
            "POST",
            "/chats",
            {},
            201,
            {"1": {"messages": None, "users": None}},
        ],
        [
            "PUT",
            "/chats",
            None,
            405,
            {"message": "PUT not supported for resource /chats."},
        ],
        [
            "DELETE",
            "/chats",
            None,
            405,
            {"message": "DELETE not supported for resource /chats."},
        ],
        # Outer Dictionary persistance tests
        [
            "POST",
            "/chats",
            {},
            201,
            {"2": {"messages": None, "users": None}},
        ],
        [
            "GET",
            "/chats",
            None,
            200,
            {
                "1": {"messages": None, "users": None},
                "2": {"messages": None, "users": None},
            },
        ],
    ],
)
def test_curl(client, operation, param, path, expected_code, expected_response):
    """All tests above must be performed in sequenece for correctness"""
    response = perform_curl_op(client, operation, param, path)

    print(response.json)

    assert response.status_code == expected_code
    assert response.json == expected_response
