import pytest
import requests
from data.data_URL import url
from data.courier_data import register_new_courier_and_return_login_password

@pytest.fixture
def registered_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    courier_data = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }
    yield courier_data  # Удаление курьера после теста

    # Delete the created courier
    login_payload = {"login": courier_data["login"], "password": courier_data["password"]}
    login_response = requests.post(f"{url}/api/v1/courier/login", data=login_payload)
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            delete_response = requests.delete(f"{url}/api/v1/courier/{courier_id}")
            assert delete_response.status_code == 200, f"Failed to delete courier. Status: {delete_response.status_code}"


@pytest.fixture
def delete_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    courier_data = {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    yield courier_data  # После теста выполняем удаление

    login_payload = {"login": courier_data["login"], "password": courier_data["password"]}
    login_response = requests.post(f"{url}/api/v1/courier/login", data=login_payload)
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")