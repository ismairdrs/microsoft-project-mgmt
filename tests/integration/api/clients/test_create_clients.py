from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_client_success(
    async_client,
):
    payload = {
        "name": "Ismair Junior",
        "email": "test@gmail.com",
        "phone": "62981888888",
    }
    response = await async_client.post("/clients", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Ismair Junior"
    assert body["email"] == "test@gmail.com"
    assert body["phone"] == "62981888888"
    assert body["created_at"] is not None


@pytest.mark.asyncio
async def test_create_client_email_duplicate(async_client):
    payload = {
        "name": "Ismair Junior",
        "email": "test@gmail.com",
        "phone": "62981888888",
    }

    response1 = await async_client.post("/clients", json=payload)
    assert response1.status_code == HTTPStatus.CREATED

    response2 = await async_client.post("/clients", json=payload)
    assert response2.status_code == HTTPStatus.BAD_REQUEST
    assert response2.json() == {
        'code': 400,
        'errors': [],
        'message': 'Client already exists in the database',
        'type': 'CLIENT_ALREADY_EXISTS',
    }


@pytest.mark.asyncio
async def test_create_client_missing_fields(async_client):
    payload = {
        "name": "Ismair Junior",
    }

    response = await async_client.post("/clients", json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        'detail': [
            {
                'input': {'name': 'Ismair Junior'},
                'loc': ['body', 'email'],
                'msg': 'Field required',
                'type': 'missing',
            },
            {
                'input': {'name': 'Ismair Junior'},
                'loc': ['body', 'phone'],
                'msg': 'Field required',
                'type': 'missing',
            },
        ]
    }
