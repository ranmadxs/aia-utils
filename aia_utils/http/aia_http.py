import requests
import os
import json
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)
# Limitar pymongo a solo errores
logging.getLogger('pymongo').setLevel(logging.ERROR)
class AiaHttpClient:
    def __init__(self) -> None:
        self.use_cache = os.getenv('AIA_HTTP_CACHE', 'false').lower() == 'true'
        self.cache_ttl = int(os.getenv('AIA_HTTP_CACHE_TTL', '3600'))  # Default 1 hour
        if self.use_cache:
            self.mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
            self.db = self.mongo_client['aia_http_cache']
            self.cache_collection = self.db['http_requests']

    def _get_cache_key(self, url, headers=None, params=None, data=None, json_data=None):
        """Generate a unique cache key based on the request parameters."""
        cache_data = {
            'url': url,
            'headers': headers,
            'params': params,
            'data': data,
            'json': json_data
        }
        return json.dumps(cache_data, sort_keys=True)

    def _is_cache_valid(self, cached_response):
        """Check if the cached response is still valid based on TTL."""
        if not cached_response or 'timestamp' not in cached_response:
            return False
        
        cache_time = cached_response['timestamp']
        # Asegurar que ambas fechas tengan zona horaria
        if cache_time.tzinfo is None:
            cache_time = cache_time.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        
        age = current_time - cache_time
        return age.total_seconds() < self.cache_ttl

    def _get_from_cache(self, cache_key):
        """Retrieve response from cache if it exists and is valid."""
        if not self.use_cache:
            return None
        
        cached_response = self.cache_collection.find_one({'cache_key': cache_key})
        
        if cached_response and self._is_cache_valid(cached_response):
            logger.debug(f"[AiaHttpClient] Cache HIT for key: {cache_key}")
            # Reconstruct response object from cached data
            response_data = cached_response.get('response')
            response = requests.Response()
            response.status_code = response_data.get('status_code')
            response._content = response_data.get('content').encode() if response_data.get('content') else None
            response.headers = response_data.get('headers', {})
            return response
        
        if cached_response:
            logger.debug(f"[AiaHttpClient] Cache EXPIRED for key: {cache_key}")
        else:
            logger.debug(f"[AiaHttpClient] Cache MISS for key: {cache_key}")
        return None

    def _save_to_cache(self, cache_key, response):
        """Save response to cache with current timestamp."""
        if not self.use_cache:
            return
        
        # Store only serializable response data
        response_data = {
            'status_code': response.status_code,
            'content': response.text,
            'headers': dict(response.headers)
        }
        
        cache_entry = {
            'cache_key': cache_key,
            'response': response_data,
            'timestamp': datetime.now(timezone.utc)
        }
        
        self.cache_collection.update_one(
            {'cache_key': cache_key},
            {'$set': cache_entry},
            upsert=True
        )
        logger.debug(f"[AiaHttpClient] Response cached for key: {cache_key} with TTL: {self.cache_ttl} seconds")

    def get(self, url, headers=None, params=None):
        cache_key = self._get_cache_key(url, headers, params)
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            return cached_response
        logger.debug(f"[AiaHttpClient] Performing HTTP GET: {url} (no cache)")
        response = requests.get(url, headers=headers, params=params)
        self._save_to_cache(cache_key, response)
        return response
    
    def post(self, url, headers=None, params=None, data=None, json=None):
        cache_key = self._get_cache_key(url, headers, params, data, json)
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            return cached_response
        logger.debug(f"[AiaHttpClient] Performing HTTP POST: {url} (no cache)")
        response = requests.post(url, headers=headers, params=params, data=data, json=json)
        self._save_to_cache(cache_key, response)
        return response
    