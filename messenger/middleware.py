from asgiref.sync import sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

from config import settings

User = get_user_model()


class WebSocketAuthMiddleware:
    """Мидлварь для аутентификации пользователей по сессии через WebSocket"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем sessionid из cookies
        headers = dict(scope.get("headers", []))
        session_id = None

        if b"cookie" in headers:
            cookies = headers[b"cookie"].decode()
            cookies_dict = dict(cookie.split("=", 1) for cookie in cookies.split("; ") if "=" in cookie)
            session_id = cookies_dict.get(settings.SESSION_COOKIE_NAME)

        # Проверяем, есть ли session_id
        if session_id:
            user = await self.get_user_from_session(session_id)
            scope["user"] = user
        else:
            scope["user"] = None

        return await self.app(scope, receive, send)

    @sync_to_async
    def get_user_from_session(self, session_id):
        """Получаем пользователя из сессии."""
        try:
            session = Session.objects.get(session_key=session_id)
            user_id = session.get_decoded().get("_auth_user_id")
            return User.objects.get(id=user_id)
        except (Session.DoesNotExist, User.DoesNotExist):
            return None
