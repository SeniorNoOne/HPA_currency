from time import time
from currency.choices import RequestMethodChoices
from currency.models import RequestResponseLog


class RequestResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time()
        response = self.get_response(request)
        end_time = time()
        # processing time in milliseconds
        # floating part will be truncated
        processing_time = (end_time - start_time) * 1000

        log = RequestResponseLog.objects.create(path=request.path,
                                                request_method=RequestMethodChoices[
                                                    request.method].value,
                                                time=processing_time)
        log.save()

        return response
