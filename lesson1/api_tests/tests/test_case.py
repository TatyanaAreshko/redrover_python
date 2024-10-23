import pytest

from lesson1.api_tests.case.pom.case import create_case
from lesson1.api_tests.case.models.case import Case
from lesson1.api_tests.case.data.case import create_case_dict, create_high_priority_case_dict, \
    create_medium_priority_case_dict


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


