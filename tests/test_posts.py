from app import schemas
import pytest

def test_get_all_posts(autorized_client, test_posts):
    res = autorized_client.get("/posts/")
    def validate(post):
        #print(schemas.PostOut(**post))
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    post_list = list(post_map)
    # print(post_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert post_list[0].Post.id == test_posts[1].id # error in getting the correct post id, its all inverted 


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(autorized_client, test_posts):
    res = autorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(autorized_client, test_posts):
    res = autorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("fav title", "fav content", True)
])

def test_create_post(autorized_client, test_user, test_posts, title, content, published):
    res = autorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(autorized_client, test_user, test_posts):
    res = autorized_client.post("/posts/", json={"title": "kadgflba", "content": "ahsdgb", })

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "kadgflba"
    assert created_post.content == "ahsdgb"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_one_post(client,test_user, test_posts):
    res = client.post("/posts/", json={"title": "kadgflba", "content": "ahsdgb", })
    
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client,test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
   
    assert res.status_code == 401


def test_delete_post_success(autorized_client, test_user, test_posts):
    res = autorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204


def test_delete_post_non_exist(autorized_client, test_user, test_posts):
    res = autorized_client.delete("/posts/564464546")
    
    assert res.status_code == 404


def test_delete_other_user_post(autorized_client, test_user, test_posts):
    res = autorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(autorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = autorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def update_other_user_post(autorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = autorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client,test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
   
    assert res.status_code == 401


def test_update_post_non_exist(autorized_client, test_user, test_posts):
    res = autorized_client.put("/posts/564464546")
    
    assert res.status_code == 422 