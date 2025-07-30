from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Flight
from .services import search_flights

@api_view(['GET'])
def search_flights_view(request):
    """
    Endpoint to search for flights based on user input.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the flight results.
    """
    origin = request.query_params.get('origin')
    destination = request.query_params.get('destination')
    date = request.query_params.get('date')

    if not all([origin, destination, date]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    flights = search_flights(origin, destination, date)
    return JsonResponse({'flights': flights})