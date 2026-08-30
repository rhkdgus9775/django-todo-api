from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class RegisterAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "username": "testuser",
            "password": "test1234!"
        }

        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

class JWTAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="jwtuser",
            password="test1234!"
        )

    def test_get_jwt_token(self):
        data = {
            "username": "jwtuser",
            "password": "test1234!"
        }

        response = self.client.post("/api/token/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

class TodoCreateAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="todouser",
            password="test1234!"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_todo(self):
        data = {
            "text": "자동화 테스트 Todo",
            "completed": False
        }

        response = self.client.post("/api/todos/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "자동화 테스트 Todo")
        self.assertEqual(response.data["completed"], False)

class TodoSecurityAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_a = User.objects.create_user(
            username="user_a",
            password="test1234!"
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="test1234!"
        )

    def test_cannot_access_other_users_todo(self):
        # A로 인증
        self.client.force_authenticate(user=self.user_a)

        # A의 Todo 생성
        create_response = self.client.post(
            "/api/todos/",
            {
                "text": "A의 비밀 Todo",
                "completed": False
            },
            format="json"
        )

        todo_id = create_response.data["id"]

        # B로 인증 사용자 변경
        self.client.force_authenticate(user=self.user_b)

        # B가 A의 Todo에 접근 시도
        response = self.client.get(
            f"/api/todos/{todo_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
