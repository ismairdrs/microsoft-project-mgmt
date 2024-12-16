from http import HTTPStatus

import pytest

from tests.utils.database import DatabaseUtils
from tests.utils.factories.client import DBClientFactory
from tests.utils.factories.project import DBProjectFactory


@pytest.mark.asyncio
async def test_create_activity_success(async_client, db):
    db_client = DBClientFactory.build()
    await DatabaseUtils.create(db, db_client)

    db_project = DBProjectFactory.build(client_id=db_client.id)
    await DatabaseUtils.create(db, db_project)

    payload = {
        "name": "Activity 1",
        "description": "Description for Activity 1",
        "project_id": str(db_project.id),
    }
    response = await async_client.post("/activities", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Activity 1"
    assert body["description"] == "Description for Activity 1"
    assert body["created_at"] is not None
    assert body["project_id"] == str(db_project.id)


@pytest.mark.asyncio
async def test_create_two_activities_for_project(async_client, db):
    db_client = DBClientFactory.build()
    await DatabaseUtils.create(db, db_client)

    db_project = DBProjectFactory.build(client_id=db_client.id)
    await DatabaseUtils.create(db, db_project)

    payload = {
        "name": "Activity 1",
        "description": "Description for Activity 1",
        "project_id": str(db_project.id),
    }

    response = await async_client.post("/activities", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Activity 1"
    assert body["description"] == "Description for Activity 1"
    assert body["created_at"] is not None
    assert body["project_id"] == str(db_project.id)

    payload = {
        "name": "Activity 2",
        "description": "Description for Activity 2",
        "project_id": str(db_project.id),
    }

    response = await async_client.post("/activities", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Activity 2"
    assert body["description"] == "Description for Activity 2"
    assert body["created_at"] is not None
    assert body["project_id"] == str(db_project.id)
