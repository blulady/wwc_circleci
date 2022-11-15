from django.http import JsonResponse


def error_404(request, exception):
    message = ('Endpoint not found (404)')
    response = JsonResponse(data={'error': message})
    response.status_code = 404
    return response
