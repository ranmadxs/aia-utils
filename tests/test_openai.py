import os
import pytest
from aia_utils.http.aia_http import AiaHttpClient

@pytest.mark.skip(reason='OPENAI_API_KEY not set or invalid')
def test_openai_chat():
    # Configurar el cliente HTTP
    http_client = AiaHttpClient()
    
    # Configurar la URL y headers
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    # Configurar el payload
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "¿Cuál es la capital de Francia?"}
        ]
    }
    
    # Realizar la petición
    response = http_client.post(url, headers=headers, json=data)
    
    # Verificar la respuesta
    assert response.status_code == 200
    response_data = response.json()
    assert "choices" in response_data
    assert len(response_data["choices"]) > 0
    assert "message" in response_data["choices"][0]
    assert "content" in response_data["choices"][0]["message"]
    
    # Verificar que la respuesta contiene la información esperada
    content = response_data["choices"][0]["message"]["content"]
    assert "París" in content.lower() or "paris" in content.lower() 