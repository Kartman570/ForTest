from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from typing import Union, List

from main.models import User, Tag


class TestViewSetBase(APITestCase):
    user_attributes = {}
    user: User = None
    client: APIClient = None
    tag_attributes = {}
    tag: Tag = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.user.is_staff = True
        cls.client = APIClient()

    @classmethod
    def create_api_user(cls):
        return User.objects.create(**cls.user_attributes)

    @classmethod
    def create_test_tag(cls):
        return Tag.objects.create(**cls.tag_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        return response

    def update(self, data: dict, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.detail_url(id), data=data)
        return response

    def delete(self, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(id))
        return response

    def list(self) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url())
        return response

    def retrieve(self, id: int = None):
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(id))
        return response
