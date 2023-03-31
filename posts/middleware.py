from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.decorators import sync_and_async_middleware
from django.http import HttpResponse
from ipware import get_client_ip

BLACK_LIST = ["127.0.0.1", "localhost"]


def ip_is_valid(get_response):
    def middleware(request):
        ip, is_routable = get_client_ip(request)

        print(ip)
        print(is_routable)

        return get_response(request)

    return middleware


class IPIsValid:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)

        if ip in BLACK_LIST:
            return HttpResponse(
                f"Uy, tsorry not tzorry percanta, {ip} {is_routable}",
                status=404,
            )

        return self.get_response(request)


class MiddlewareEjemplar:
    def __init__(self, get_response):
        """Método de inicialización del middleware. Llamado una sola vez,
        al momento de instanciar el middleware.

        Args:
            get_response (HttpResponse): Un empaquetamiento del response,
            que representa lo que viene después del middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Código que es llamado cada vez que se ejecuta una petición."""
        response = self.get_response(request)
        return response

    def process_view(request, view_func, view_args, view_kwargs):
        """Método invocado por Django justo antes de llamar a la vista.

        Args:
            request (HttpRequest): El objeto que representa la petición.
            view_func (func): Es la función Python que Django va a utilizar.
            view_args (list): Una lista de argumentos posicionales que se
                              pasarán a la vista.
            view_kwargs (dict): Objeto que se pasará a la vista.
        """
        return None

    def process_exception(request, exception):
        """Método invocado por Django cuando ocurre una excepción.

        Args:
            request (HttpRequest): El objeto que representa la petición.
            exception (Exception): La excepción que se ha lanzado.
        """
        return None

    def process_template_response(request, response):
        """Método invocado por Django cuando se ha generado un response con
        una plantilla.

        Args:
            request (HttpRequest): El objeto que representa la petición.
            response (TemplateResponse): El objeto que representa el response.
        """
        return response


@sync_and_async_middleware
def simple_middleware(get_response):
    # One-time configuration and initialization goes here.
    if iscoroutinefunction(get_response):

        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            return response

    else:

        def middleware(request):
            # Do something here!
            response = get_response(request)
            return response

    return middleware


class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        # Some logic ...
        return response
