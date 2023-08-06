from kfsd.apps.core.auth.token import TokenUser


class KubefacetsTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.token = TokenUser(request)
        response = self.get_response(request)
        return response
