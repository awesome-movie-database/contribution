__all__ = (
    "movie_contribution_requests_router",
    "person_contribution_requests_router",
)

from .movie_contribution_requests import (
    router as movie_contribution_requests_router,
)
from .person_contribution_requests import (
    router as person_contribution_requests_router,
)
