import pytest
from django.db.models import Count
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from buyer.models import Buyer
from showroom.models import ShowRoom
from fabric.models import Transaction


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def buyer_factory():
    return mixer.blend(Buyer)


# Buyer Tests


@pytest.mark.django_db
def test_buyer_list_create_view(api_client):
    url = "/buyers/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_buyer_create_view(api_client):
    create_data = {
        "name": "Buyer",
        "location": "US",
    }
    url = "/buyers/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Buyer.objects.filter(name=create_data["name"]).exists()


@pytest.mark.django_db
def test_buyer_update_view(api_client, buyer_factory):
    buyer = buyer_factory
    update_data = {
        "name": "Updated Buyer",
        "location": "BY",
    }
    url = f"/buyers/update/{buyer.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    buyer.refresh_from_db()
    assert buyer.name == "Updated Buyer"
    assert buyer.location == "BY"


@pytest.mark.django_db
def test_buyer_delete_view(api_client, buyer_factory):
    buyer = buyer_factory
    url = f"/buyers/delete/{buyer.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    buyer.refresh_from_db()
    assert not buyer.is_active


# Transaction Tests


@pytest.mark.django_db
def test_transaction_create_view(api_client, buyer_factory):
    buyer = buyer_factory
    showroom = mixer.blend(ShowRoom)
    assert ShowRoom.objects.get(id=showroom.id).buyers.count() == 0
    create_data = {
        "buyer": buyer.id,
        "showroom": showroom.id,
        "model": "Car Model",
        "price": 10000,
    }
    url = "/buyers/transaction/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Transaction.objects.filter(model=create_data["model"]).exists()
    assert ShowRoom.objects.get(id=showroom.id).buyers.count() == 1
