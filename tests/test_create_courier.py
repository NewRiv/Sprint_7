import requests
import allure

from conftest import registered_courier_data
from data.data_URL import url
from data.courier_data import generation_new_data_courier

import logging




class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и текст - "ok": True')
    def test_create_courier(self, registered_courier_data):
        data = generation_new_data_courier()
        data.pop("firstName")
        payload = data
        logging.info(f"Data for courier creation: {data}")


        response = requests.post(f"{url}/api/v1/courier", data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."

        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f"{url}/api/v1/courier/login", data=login_payload)
        assert login_response.status_code == 200, "Login failed."

        courier_id = login_response.json().get("id")
        assert courier_id is not None, f"Курьер с идентификатором {courier_id} не найден"


    @allure.title('Проверка невозможности создать курьера. дублирующие креды')
    @allure.description('Проверка, что нельзя создать курьера с уже существующеми кредами (код - 409 и текст - "message": "Этот логин уже используется. Попробуйте другой."')
    def test_create_courier_duplicate_login(self, registered_courier_data):
        payload = registered_courier_data
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}, "Неверное содержимое ответа."


    @allure.title('Проверка невозможности создать курьера. Не все обязательные поля')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 400 и текст - "message": "Недостаточно данных для создания учетной записи"')
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}, "Неверное содержимое ответа."
