import pytest
from jose import jwt
from app import schemas

SECRET_KEY = "zmqEwYe26ESSqU6jbiJwRnwxvFPgJfYM"
ALGORITHM = 'HS256'



#simple, testing root test 
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World!!'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password123"})
    #we can use schemas to verify 
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=ALGORITHM)
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@email.com', 'password123', 403),
    ('test@gmail.com', 'wrongpassword', 403),
    ('wrongemail', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code==status_code
    # assert res.json().get('detail') == "Invalid Credentials"