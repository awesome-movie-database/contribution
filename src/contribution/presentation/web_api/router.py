from fastapi import APIRouter

from .routers import (
    movie_contribution_requests_router,
    person_contribution_requests_router,
)


router = APIRouter(prefix="/v1")

router.include_router(movie_contribution_requests_router)
router.include_router(person_contribution_requests_router)
