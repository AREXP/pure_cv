import pytest

GET_SQL = 'SELECT status, token FROM users WHERE token = $1'


@pytest.mark.parametrize(
    ['body', 'auth'],
    [
        pytest.param(
            {'online': True},
            {'token':'token1'},
            id='set true status',
        ),
        pytest.param(
            {'online': True},
            {'token': 'token2'},
            id='set true status',
        ),
    ],
)
async def test_me(test_client, body, auth):
    resp = await test_client.post('/api/me', json=body, headers=auth)
    assert resp.status == 200

    async with test_client.app.pg_pool.acquire() as connection:
        row = await connection.fetchrow(GET_SQL, auth['token'])

    assert row['status'] == body['online']


@pytest.mark.parametrize(
    ['body', 'auth', 'expected_status', 'expected_msg'],
    [
        pytest.param(
            {},
            {'token': 'token1'},
            400,
            'online status is not provided',
            id='no status provided',
        ),
        pytest.param(
            {'online': True},
            {},
            401,
            'token is not provided',
            id='set true status',
        ),
    ],
)
async def test_me_fail(test_client, body, auth, expected_status, expected_msg):
    resp = await test_client.post('/api/me', json=body, headers=auth)
    assert resp.status == expected_status

    json = await resp.json()
    assert json['msg'] == expected_msg
