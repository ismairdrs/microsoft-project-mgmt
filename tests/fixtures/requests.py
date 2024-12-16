from unittest.mock import Mock

import pytest


@pytest.fixture
def starlette_request_scope():
    return {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "server": ("127.0.0.1", 8000),
        "client": ("127.0.0.1", 59362),
        "scheme": "http",
        "method": "POST",
        "root_path": "",
        "path": "/scr",
        "raw_path": b"/scr",
        "query_string": b"",
        "headers": [
            (b"authorization", b"Bearer token"),
            (b"content-type", b"application/json"),
            (b"user-agent", b"SomeBrowser/1.1.1"),
            (b"accept", b"*/*"),
            (b"postman-token", b"d085f219-14d2-4014-b06b-42ae38df88e0"),
            (b"host", b"localhost:8000"),
            (b"accept-encoding", b"gzip, deflate, br"),
            (b"connection", b"keep-alive"),
            (b"content-length", b"80"),
        ],
        "app": Mock(),
    }
