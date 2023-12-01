import pytest
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer

from fabric.models import Fabric, FabricCars


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fabric_factory():
    return mixer.blend(Fabric)


@pytest.fixture
def fabric_cars_factory():
    return mixer.blend(FabricCars)


# Fabric Tests


@pytest.mark.django_db
def test_fabric_list_view(api_client):
    url = "/fabrics/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_fabric_create_view(api_client):
    create_data = {
        "name": "Fabric",
        "location": "US",
        "capacity": 100,
    }
    url = "/fabrics/create/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Fabric.objects.filter(name=create_data["name"]).exists()


@pytest.mark.django_db
def test_fabric_update_view(api_client, fabric_factory):
    fabric = fabric_factory
    update_data = {
        "name": "Updated Fabric",
        "location": "AF",
    }
    url = f"/fabrics/update/{fabric.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    fabric.refresh_from_db()
    assert fabric.name == "Updated Fabric"
    assert fabric.location == "AF"


@pytest.mark.django_db
def test_fabric_delete_view(api_client, fabric_factory):
    fabric = fabric_factory
    url = f"/fabrics/delete/{fabric.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    fabric.refresh_from_db()
    assert not fabric.is_active


@pytest.mark.django_db
def test_fabric_update_view_invalid_data(api_client, fabric_factory):
    fabric = fabric_factory
    update_data = {
        "name": "",
    }
    url = f"/fabrics/update/{fabric.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_fabric_delete_view_invalid_id(api_client):
    invalid_id = 999
    url = f"/fabrics/delete/{invalid_id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# FabricCars Tests


@pytest.mark.django_db
def test_fabric_cars_create_view(api_client, fabric_factory):
    fabric = fabric_factory
    create_data = {
        "model": "Car Model",
        "price": 10000,
        "amount": 5,
        "year_ofrelease": 2022,
        "fabric": fabric.id,
    }
    url = "/fabrics_cars/create/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert FabricCars.objects.filter(model=create_data["model"]).exists()


@pytest.mark.django_db
def test_fabric_cars_update_view(api_client, fabric_cars_factory):
    fabric_cars = fabric_cars_factory
    update_data = {
        "price": 12000,
        "year_of_release": 2020,
        "model": "tesla",
    }
    url = f"/fabrics_cars/update/{fabric_cars.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    fabric_cars.refresh_from_db()
    assert fabric_cars.price == 12000
    assert fabric_cars.year_of_release == 2020
    assert fabric_cars.model == "tesla"


@pytest.mark.django_db
def test_fabric_cars_delete_view(api_client, fabric_cars_factory):
    fabric_cars = fabric_cars_factory
    url = f"/fabrics_cars/delete/{fabric_cars.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    fabric_cars.refresh_from_db()
    assert not fabric_cars.is_active
