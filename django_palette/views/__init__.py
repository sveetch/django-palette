from django.http import JsonResponse, HttpResponseBadRequest


class JsonResponseBadRequest(JsonResponse):
    """
    JSON response with a Bad request status code
    """
    status_code = HttpResponseBadRequest.status_code
