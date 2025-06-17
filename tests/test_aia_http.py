import pytest
from aia_utils.http.aia_http import AiaHttpClient

@pytest.fixture
def http_client():
    return AiaHttpClient()

# poetry run pytest tests/test_aia_http.py::test_get -s
def test_get(http_client):
    # Test GET request to a public API
    response = http_client.get("https://jsonplaceholder.typicode.com/posts/3")
    
    # Assert response status code
    assert response.status_code == 200
    
    # Assert response content
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert "title" in data
    assert "body" in data

# poetry run pytest tests/test_aia_http.py::test_post -s
def test_post(http_client):
    # Test POST request to a public API
    test_data = {
        "title": "Test Title",
        "body": "Test Body",
        "userId": 1
    }
    
    response = http_client.post(
        "https://jsonplaceholder.typicode.com/posts",
        data=test_data
    )
    
    # Assert response status code
    assert response.status_code == 201
    
    # Assert response content
    data = response.json()
    assert isinstance(data, dict)
    assert data["title"] == test_data["title"]
    assert data["body"] == test_data["body"]
    assert int(data["userId"]) == test_data["userId"]
    assert "id" in data

# poetry run pytest tests/test_aia_http.py::test_gemini -s
def test_gemini(http_client):
    # Test POST request to Gemini API
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyA_7-Pyu5ZccduTVnSktUTji4NvlIDNYh8"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "me puedes dar las estadísticas base para  https://wahapedia.ru/wh40k10ed/factions/space-marines/Lieutenant-Titus. "
                    }
                ]
            }
        ]
    }
    
    response = http_client.post(url, headers=headers, json=payload)
    
    # Assert response status code
    assert response.status_code == 200
    
    # Print the response text to console
    print(response.text)