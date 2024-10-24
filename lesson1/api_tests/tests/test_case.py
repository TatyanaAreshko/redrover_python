import pytest

from lesson1.api_tests.case.pom.case import create_case
from lesson1.api_tests.case.models.case import Case
from lesson1.api_tests.case.data.case import create_case_dict, create_high_priority_case_dict, \
    create_medium_priority_case_dict
from lesson1.api_tests.utils.api_client import client
import json

##learning how to create a test using dict
def test_create_case_with_low_priority():
    response = create_case(Case(**create_case_dict).model_dump())
    response.status_code_should_be_eq(200)
    response.json_should_be_eq(Case(**create_case_dict).model_dump())
    response.schema_should_be_eq(Case(**create_case_dict).model_json_schema())

def test_create_case_with_high_priority():
    response = create_case(Case(**create_high_priority_case_dict).model_dump())
    response.status_code_should_be_eq(200)
    response.json_should_be_eq(Case(**create_high_priority_case_dict).model_dump())
    response.schema_should_be_eq(Case(**create_high_priority_case_dict).model_json_schema())

@pytest.mark.xfail
def test_create_case_with_medium_priority():
    response = create_case(Case(**create_medium_priority_case_dict).model_dump())
    response.status_code_should_be_eq(200)
    response.json_should_be_eq(Case(**create_medium_priority_case_dict).model_dump())
    response.schema_should_be_eq(Case(**create_medium_priority_case_dict).model_json_schema())

##learning how to create a test using api client
def test_create_empty_case():
    response = client.make_request(handle="/testcases", method="POST", json={})
    response.status_code_should_be_eq(422)

def test_create_case():
    response = client.make_request(handle="/testcases", method="POST",
        json={
    "id": 1,
    "name": "Имя",
    "description": "Описание",
    "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
    "expected_result": "Ожидаемый результат",
    "priority": "низкий",
})
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(1)

def test_get_created_case_by_id():
    response = client.make_request(handle="/testcases", method="POST",
        json={
            "id": 111,
            "name": "Имя",
            "description": "Описание",
            "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
            "expected_result": "Ожидаемый результат",
            "priority": "низкий",
        })
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(111)
    case_id = response.get_value_with_key("id")

    response = client.make_request(handle=f"/testcases/{case_id}", method="GET")
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(111)
    response.value_with_key("name").should_be_eq("Имя")

def test_update_case():
    response = client.make_request(handle="/testcases", method="POST",
                                   json={
                                       "id": 222,
                                       "name": "Имя",
                                       "description": "Описание",
                                       "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
                                       "expected_result": "Ожидаемый результат",
                                       "priority": "низкий",
                                   })
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(222)
    case_id = response.get_value_with_key("id")

    response = client.make_request(handle=f"/testcases/{case_id}", method="PUT",
                                   json={
                                       "id": 222,
                                       "name": "Имя",
                                       "description": "Обновили тесткейс",
                                       "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
                                       "expected_result": "Ожидаемый результат",
                                       "priority": "низкий",
                                   })
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(222)
    response.value_with_key("description").should_be_eq("Обновили тесткейс")

def test_delete_case():
    response = client.make_request(handle="/testcases", method="POST",
                                   json={
                                       "id": 333,
                                       "name": "Имя",
                                       "description": "Описание",
                                       "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
                                       "expected_result": "Ожидаемый результат",
                                       "priority": "низкий",
                                   })
    response.status_code_should_be_eq(200)
    response.value_with_key("id").should_be_eq(333)
    case_id = response.get_value_with_key("id")

    response = client.make_request(handle=f"/testcases/{case_id}", method="DELETE")
    response.status_code_should_be_eq(200)
    response.json_should_be_eq({"detail":"Test case deleted."})

    response = client.make_request(handle=f"/testcases/{case_id}", method="GET")
    response.status_code_should_be_eq(404)
    response.json_should_be_eq({"detail":"Test case not found."})
