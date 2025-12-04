import base64

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BasicAuthMiddleware(MiddlewareMixin):
    """Protects the entire site with HTTP Basic authentication."""

    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.lower().startswith("basic "):
            return self._unauthorized_response()

        try:
            encoded_credentials = auth_header.split(" ", 1)[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        except (IndexError, ValueError, UnicodeDecodeError, base64.binascii.Error):
            return self._unauthorized_response()

        username, password = decoded_credentials.split(":", 1) if ":" in decoded_credentials else ("", "")
        if not self._is_valid(username, password):
            return self._unauthorized_response()

        return None

    def _is_valid(self, username: str, password: str) -> bool:
        return username == "admin" and password == "Admin#184!"

    def _unauthorized_response(self) -> HttpResponse:
        response = HttpResponse("Authentication required", status=401)
        response["WWW-Authenticate"] = 'Basic realm="Restricted"'
        return response
