import time
import logging
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    """
    Middleware für Performance-Monitoring und Optimierungen
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request Start Time
        start_time = time.time()
        
        # Response generieren
        response = self.get_response(request)
        
        # Response Time berechnen
        response_time = time.time() - start_time
        
        # Performance Header hinzufügen
        response['X-Response-Time'] = f"{response_time:.3f}s"
        
        # Logging für langsame Requests
        if response_time > 1.0:  # Langsamer als 1 Sekunde
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {response_time:.3f}s"
            )
        
        return response

class CacheMiddleware:
    """
    Smart Caching Middleware für API Responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_timeout = getattr(settings, 'API_CACHE_TIMEOUT', 300)
    
    def __call__(self, request):
        # Nur GET Requests cachen
        if request.method != 'GET':
            return self.get_response(request)
        
        # Cache Key generieren
        cache_key = self._generate_cache_key(request)
        
        # Cache prüfen
        cached_response = cache.get(cache_key)
        if cached_response:
            response = JsonResponse(cached_response)
            response['X-Cache'] = 'HIT'
            return response
        
        # Response generieren
        response = self.get_response(request)
        
        # Response cachen (nur bei 200 Status)
        if response.status_code == 200 and hasattr(response, 'data'):
            cache.set(cache_key, response.data, self.cache_timeout)
            response['X-Cache'] = 'MISS'
        
        return response
    
    def _generate_cache_key(self, request):
        """Cache Key basierend auf URL und Query Parameters generieren"""
        key = f"api_cache:{request.path}"
        if request.GET:
            query_string = "&".join([f"{k}={v}" for k, v in sorted(request.GET.items())])
            key += f"?{query_string}"
        return key

class CompressionMiddleware:
    """
    Response Compression Middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Gzip Header hinzufügen für JSON Responses
        if 'application/json' in response.get('Content-Type', ''):
            response['Vary'] = 'Accept-Encoding'
        
        return response
