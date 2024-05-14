def test_get_all_posts(autorized_client):
    res = autorized_client.get("/posts/")
    print(res.json())
    return 