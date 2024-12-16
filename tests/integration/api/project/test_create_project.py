from http import HTTPStatus

import pytest

from microsoft.enums import ProjectStatus
from tests.utils.database import DatabaseUtils
from tests.utils.factories.client import DBClientFactory


@pytest.mark.asyncio
async def test_create_project_success(async_client, db):
    db_client = DBClientFactory.build()
    await DatabaseUtils.create(db, db_client)

    payload = {
        "name": "Project 1",
        "description": "Description",
        "status": ProjectStatus.OPEN.value,
        "client_id": str(db_client.id),
    }
    response = await async_client.post("/projects", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Project 1"
    assert body["description"] == "Description"
    assert body["status"] == "OPEN"
    assert body["created_at"] is not None
    assert body["client_id"] == str(db_client.id)


@pytest.mark.asyncio
async def test_create_two_project_for_client(async_client, db):
    db_client = DBClientFactory.build()
    await DatabaseUtils.create(db, db_client)

    payload = {
        "name": "Project 1",
        "description": "Description",
        "status": ProjectStatus.OPEN.value,
        "client_id": str(db_client.id),
    }
    response = await async_client.post("/projects", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Project 1"
    assert body["description"] == "Description"
    assert body["status"] == "OPEN"
    assert body["created_at"] is not None
    assert body["client_id"] == str(db_client.id)

    payload = {
        "name": "Project 2",
        "description": "Description",
        "status": ProjectStatus.OPEN.value,
        "client_id": str(db_client.id),
    }
    response = await async_client.post("/projects", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Project 2"
    assert body["description"] == "Description"
    assert body["status"] == "OPEN"
    assert body["created_at"] is not None
    assert body["client_id"] == str(db_client.id)


@pytest.mark.asyncio
async def test_create_project_without_client_id(async_client):
    payload = {
        "name": "Project 1",
        "description": "Description",
        "status": ProjectStatus.OPEN.value,
    }

    response = await async_client.post("/projects", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "input": {
                    "description": "Description",
                    "name": "Project 1",
                    "status": "OPEN",
                },
                "loc": ["body", "client_id"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_project_invalid_client_id(async_client):
    payload = {
        "name": "Project 1",
        "description": "Description",
        "status": ProjectStatus.OPEN.value,
        "client_id": "invalid-uuid",
    }

    response = await async_client.post("/projects", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "error": "invalid character: expected an optional "
                    "prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
                },
                "input": "invalid-uuid",
                "loc": ["body", "client_id"],
                "msg": "Input should be a valid UUID, invalid character: "
                "expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-],"
                " found `i` at 1",
                "type": "uuid_parsing",
            }
        ]
    }
