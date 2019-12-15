import datetime

import pytest
from freezegun import freeze_time


async def test_throttle(test_client):
    test_client.app.config['throttle_limits'] = {'second': 2}
    token = 'kkk'
    auth = {'token': token}
    body = {'online': True}

    with freeze_time('2019-12-14'):
        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 200

        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 200

        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 409


async def test_throttle_erase(test_client):
    test_client.app.config['throttle_limits'] = {'second': 2}
    token = 'kkk1'
    auth = {'token': token}
    body = {'online': True}
    false_body = {'online': False}

    with freeze_time('2019-12-14'):
        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 200

        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 200

        resp = await test_client.post('/api/me', json=false_body, headers=auth)
        assert resp.status == 200

        resp = await test_client.post('/api/me', json=body, headers=auth)
        assert resp.status == 200
