import pytest
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient

from showroom.models import ShowRoom
from showroom.model_cars import ShowRoomCars


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def showroom_factory():
    return mixer.blend(ShowRoom)


@pytest.fixture
def showroom_cars_factory():
    return mixer.blend(ShowRoomCars)


@pytest.mark.django_db
def test_showroom_list_view(api_client):
    url = "/showrooms/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


# ShowRoom tests
@pytest.mark.django_db
def test_showroom_create_view(api_client):
    create_data = {
        "name": "Showroom",
        "location": "AF",
        "min_price": 500,
        "max_price": 2000,
        "min_year_of_release": 2000,
        "max_year_of_release": 2022,
    }
    url = "/showrooms/create/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ShowRoom.objects.filter(name=create_data["name"]).exists()


@pytest.mark.django_db
def test_showroom_update_view(api_client, showroom_factory):
    showroom = showroom_factory
    update_data = {
        "name": "Updated Showroom",
        "min_price": 600,
        "location": "AF",
        "max_price": 1200,
        "min_year_of_release": 2000,
        "max_year_of_release": 2020,
    }
    url = f"/showrooms/update/{showroom.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    showroom.refresh_from_db()
    assert showroom.name == "Updated Showroom"
    assert showroom.min_price == 600
    assert showroom.location == "AF"
    assert showroom.max_year_of_release == 2020


@pytest.mark.django_db
def test_showroom_delete_view(api_client, showroom_factory):
    showroom = showroom_factory
    url = f"/showrooms/delete/{showroom.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    showroom.refresh_from_db()
    assert not showroom.is_active


@pytest.mark.django_db
def test_showroom_update_view_invalid_data(api_client, showroom_factory):
    showroom = showroom_factory
    update_data = {
        "name": "",
    }
    url = f"/showrooms/update/{showroom.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_showroom_delete_view_invalid_id(api_client):
    invalid_id = 999
    url = f"/showrooms/delete/{invalid_id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ShowRoomCars tests


@pytest.mark.django_db
def test_showroom_cars_create_view(api_client, showroom_factory):
    showroom = showroom_factory
    create_data = {
        "model": "Car Model",
        "price": 10000,
        "amount": 5,
        "year_ofrelease": 2022,
        "show_room": showroom.id,
    }
    url = "/showrooms_cars/create/"
    response = api_client.post(url, data=create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ShowRoomCars.objects.filter(model=create_data["model"]).exists()


@pytest.mark.django_db
def test_showroom_cars_update_view(api_client, showroom_cars_factory):
    showroom_cars = showroom_cars_factory
    update_data = {
        "price": 12000,
        "amount": 8,
    }
    url = f"/showrooms_cars/update/{showroom_cars.id}/"
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    showroom_cars.refresh_from_db()
    assert showroom_cars.price == 12000
    assert showroom_cars.amount == 8


@pytest.mark.django_db
def test_showroom_cars_delete_view(api_client, showroom_cars_factory):
    showroom_cars = showroom_cars_factory
    url = f"/showrooms_cars/delete/{showroom_cars.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    showroom_cars.refresh_from_db()
    assert not showroom_cars.is_active
