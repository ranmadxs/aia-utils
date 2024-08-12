from aia_utils.http.aia_http import AiaHttpClient



#poetry run pytest tests/test_aia_http.py::test_get -s
def test_get():
    print("Test get")
    http_client = AiaHttpClient()
    response = http_client.get("https://jsonplaceholder.typicode.com/posts/1")
    print(response.json())
    print(response.status_code)
    assert response.status_code == 200