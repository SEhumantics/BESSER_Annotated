import pytest
import requests
import json

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def post_class():
    def _post_class(name, properties, methods, is_abstract=False, is_read_only=False):
        url = f"{BASE_URL}/classes/"
        payload = {
            "name": name,
            "properties": properties,
            "methods": methods,
            "is_abstract": is_abstract,
            "is_read_only": is_read_only
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json(), response.status_code
    return _post_class

@pytest.fixture
def post_enumeration():
    def _post_enumeration(name, literals):
        url = f"{BASE_URL}/enumerations/"
        payload = {
            "name": name,
            "literals": literals
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json(), response.status_code
    return _post_enumeration

@pytest.fixture
def post_association():
    def _post_association(name, ends):
        url = f"{BASE_URL}/associations/"
        payload = {
            "name": name,
            "ends": ends
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json(), response.status_code
    return _post_association

@pytest.fixture
def post_domain_model():
    def _post_domain_model(name, types, associations, generalizations=[], enumerations=[], packages=[], constraints=[]):
        url = f"{BASE_URL}/domainmodels/"
        payload = {
            "name": name,
            "types": types,
            "associations": associations,
            "generalizations": generalizations,
            "enumerations": enumerations,
            "packages": packages,
            "constraints": constraints
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json(), response.status_code
    return _post_domain_model

@pytest.fixture
def get_domain_model():
    def _get_domain_model(model_id):
        url = f"{BASE_URL}/domainmodels/{model_id}"
        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json(), response.status_code
    return _get_domain_model

@pytest.fixture
def generate_pydantic_code():
    def _generate_pydantic_code(model_id):
        url = f"{BASE_URL}/pydantic/{model_id}"
        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json(), response.status_code
    return _generate_pydantic_code

def test_post_class(post_class):
    library_properties = [
        {
            "name": "nblivre",
            "property_type": "int",
            "multiplicity": [1, 1],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        },
        {
            "name": "address",
            "property_type": "str",
            "multiplicity": [1, 1],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        }
    ]
    library_methods = [
        {
            "name": "get_info",
            "visibility": "public",
            "is_abstract": False,
            "parameters": [
                {
                    "name": "include_address",
                    "parameter_type": "bool"
                },
                {
                    "name": "format",
                    "parameter_type": "str"
                }
            ],
            "type": "str",
            "code": "if include_address:\n    return f'Library at {self.address} has {self.nblivre} books'\nelse:\n    return f'Library has {self.nblivre} books'"
        }
    ]
    response, status_code = post_class("Library", library_properties, library_methods)
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "message" in response
    assert response["message"] == "Class stored successfully"

def test_post_enumeration(post_enumeration):
    response, status_code = post_enumeration("genre", ["horror", "funny"])
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "message" in response
    assert response["message"] == "Enumeration stored successfully"

def test_post_book_class(post_class):
    book_properties = [
        {
            "name": "pages",
            "property_type": "int",
            "multiplicity": [1, 1],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        },
        {
            "name": "genre",
            "property_type": "genre",
            "multiplicity": [1, 1],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        }
    ]
    response, status_code = post_class("Book", book_properties, [])
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "message" in response
    assert response["message"] == "Class stored successfully"

def test_post_association(post_association):
    association_ends = [
        {
            "name": "has",
            "property_type": "Library",
            "multiplicity": [1, "*"],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        },
        {
            "name": "in",
            "property_type": "Book",
            "multiplicity": [0, 1],
            "visibility": "public",
            "is_composite": False,
            "is_navigable": False,
            "is_id": False,
            "is_read_only": False
        }
    ]
    response, status_code = post_association("lib-book", association_ends)
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "message" in response
    assert response["message"] == "Association stored successfully"

def test_post_domain_model(post_domain_model):
    response, status_code = post_domain_model(
        name="LibraryBookModel",
        types=["Library", "Book"],
        associations=["lib-book"],
        enumerations=["genre"]
    )
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "message" in response
    assert response["message"] == "Domain Model stored successfully"

def test_get_domain_model(get_domain_model):
    domain_model_id = 1
    response, status_code = get_domain_model(domain_model_id)
    print("Response:", response)
    print("Status code:", status_code)
    assert status_code == 200
    assert "domain_model" in response