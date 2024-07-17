__all__ = (
    "setup_routes",
    "setup_middleware",
    "setup_exception_handlers",
)

from .main_router import setup_routes
from .middleware import setup_middleware
from .exception_handlers import setup_exception_handlers
