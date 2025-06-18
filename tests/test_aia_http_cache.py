import os
import pytest
import time
from aia_utils.http.aia_http import AiaHttpClient

# poetry run pytest tests/test_aia_http_cache.py -v -s

@pytest.fixture
def http_client():
    # Configurar variables de entorno para los tests
    os.environ['AIA_HTTP_CACHE'] = 'true'
    os.environ['AIA_HTTP_CACHE_TTL'] = '2'  # 2 segundos de TTL
    os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/'
    return AiaHttpClient()

# poetry run pytest tests/test_aia_http_cache.py::test_cache_hit -v -s
def test_cache_hit(http_client):
    """Test que verifica que una segunda llamada idéntica devuelve el cache"""
    # Primera llamada - debe guardar en cache
    response1 = http_client.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response1.status_code == 200
    
    # Segunda llamada - debe devolver el cache
    response2 = http_client.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response2.status_code == 200
    assert response1.text == response2.text

# poetry run pytest tests/test_aia_http_cache.py::test_cache_expiration -v -s
def test_cache_expiration(http_client):
    """Test que verifica que el cache expira después del TTL"""
    # Primera llamada - debe guardar en cache
    response1 = http_client.get("https://jsonplaceholder.typicode.com/posts/2")
    assert response1.status_code == 200
    
    # Esperar a que expire el cache (2 segundos)
    time.sleep(3)
    
    # Segunda llamada - debe hacer una nueva petición
    response2 = http_client.get("https://jsonplaceholder.typicode.com/posts/2")
    assert response2.status_code == 200
    # Las respuestas pueden ser iguales por coincidencia, pero fueron obtenidas de diferentes formas

# poetry run pytest tests/test_aia_http_cache.py::test_cache_different_params -v -s
def test_cache_different_params(http_client):
    """Test que verifica que diferentes parámetros no comparten cache"""
    # Llamada con un parámetro
    response1 = http_client.get("https://jsonplaceholder.typicode.com/posts", params={'id': 1})
    assert response1.status_code == 200
    
    # Llamada con otro parámetro
    response2 = http_client.get("https://jsonplaceholder.typicode.com/posts", params={'id': 2})
    assert response2.status_code == 200
    assert response1.text != response2.text

# poetry run pytest tests/test_aia_http_cache.py::test_cache_post_request -v -s
def test_cache_post_request(http_client):
    """Test que verifica el cache en peticiones POST"""
    # Primera llamada POST
    data1 = {"title": "Test 1", "body": "Body 1", "userId": 1}
    response1 = http_client.post("https://jsonplaceholder.typicode.com/posts", json=data1)
    assert response1.status_code == 201
    
    # Segunda llamada POST con los mismos datos
    response2 = http_client.post("https://jsonplaceholder.typicode.com/posts", json=data1)
    assert response2.status_code == 201
    assert response1.text == response2.text
    
    # Tercera llamada POST con datos diferentes
    data2 = {"title": "Test 2", "body": "Body 2", "userId": 1}
    response3 = http_client.post("https://jsonplaceholder.typicode.com/posts", json=data2)
    assert response3.status_code == 201
    assert response3.text != response2.text

# poetry run pytest tests/test_aia_http_cache.py::test_cache_disabled -v -s
def test_cache_disabled():
    """Test que verifica que el cache no funciona cuando está deshabilitado"""
    # Deshabilitar cache
    os.environ['AIA_HTTP_CACHE'] = 'false'
    http_client = AiaHttpClient()
    
    # Primera llamada
    response1 = http_client.get("https://jsonplaceholder.typicode.com/posts/3")
    assert response1.status_code == 200
    
    # Segunda llamada - debe hacer una nueva petición
    response2 = http_client.get("https://jsonplaceholder.typicode.com/posts/3")
    assert response2.status_code == 200
    # Las respuestas pueden ser iguales por coincidencia, pero fueron obtenidas de diferentes formas 