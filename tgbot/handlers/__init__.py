"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .inline import inline_router
from .users import user_router
from .channel import channel_router

routers_list = [
    admin_router,
    user_router,
    channel_router,
    inline_router
]

__all__ = ["routers_list"]
