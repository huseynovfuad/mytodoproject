from django.urls import path
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from todopost.consumers import CommentConsumer

application = ProtocolTypeRouter({
    'websocket' :  AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('post/<int:post_id>/',CommentConsumer),
            ])
        )
    )
})
