import logging
from django.test import TestCase
from django.urls import reverse
from api.services import Serializing
from users.models import User
from django.db import connection


logger = logging.getLogger("debug")


class UserViewTest(TestCase):
    base_params = "?firstname=asd&secondname=zxc&email=harlanvova03@gmail.com&password=asdadt4tt4"

    def test_post_method(self):
        request_url = f'{reverse("user_")}{self.base_params}'
        response = self.client.post(request_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(request_url)
        self.assertEqual(response.status_code, 400)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")

        logger.debug("Tested POST method on UserView ---OK")

    def test_get_method(self):
        request_url = f'{reverse("user_")}{self.base_params}'
        response = self.client.post(request_url)
        new_user_id = Serializing.deserialize(response.data)[0]["new_user"]["id"]

        request_url = f'{reverse("user_")}'
        response = Serializing.deserialize(self.client.get(request_url).data)
        self.assertEqual(response[0]["users"][0]["id"], new_user_id)
        self.assertEqual(response[0]["success"], True)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")

        logger.debug("Tested GET method on UserView ---OK")

    def test_delete_method(self):
        request_url = f'{reverse("user_")}{self.base_params}'
        response = self.client.post(request_url)
        new_user_id = Serializing.deserialize(response.data)[0]["new_user"]["id"]

        request_url = f"{reverse('user_')}?pk={new_user_id}"
        response = self.client.delete(request_url)

        self.assertEqual(response.status_code, 200)

        request_url = f"{reverse('user_')}?pk=52"
        response = self.client.delete(request_url)
        self.assertEqual(response.status_code, 404)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")

        logger.debug("Tested DELETE method on UserView ---OK")

    def test_put_method(self):
        response = self.client.post(f"{reverse('user_')}{self.base_params}")
        new_user_id = Serializing.deserialize(response.data)[0]["new_user"]["id"]

        response = Serializing.deserialize(self.client.put(f"{reverse('user_')}?pk={new_user_id}&secondname=asd").data)
        self.assertEqual(response[0]["updated_user"]["secondname"], "asd")

        response = self.client.put(f"{reverse('user_')}?pk={new_user_id}&secondname=asd&firstname=asdasdasasdas")
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f"{reverse('user_')}secondname=asd&pk=655553")
        self.assertEqual(response.status_code, 404)

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE users_user")
        logger.debug("Tested PUT method on UserView ---OK")
