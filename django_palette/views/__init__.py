import json

from django.http import JsonResponse, HttpResponseBadRequest


class JsonResponseBadRequest(JsonResponse):
    """
    JSON response with a Bad request status code.
    """
    status_code = HttpResponseBadRequest.status_code


class JsonFormPost:
    """
    A mixin to get form data from decoded JSON request body.

    This is required to receive form data from "application/json" requests
    instead of "application/x-www-form-urlencoded" that is the only one
    supported content type to send form datas.

    DEPRECATED: When used with django test client raise:

        django.http.request.RawPostDataException: You cannot access body after
        reading from request's data stream

    Because client seems to read request body before this mixin. I was unable
    to find a solution.
    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            data = self.request.body.decode('utf-8')

            kwargs['data'] = json.loads(data)

        return kwargs


