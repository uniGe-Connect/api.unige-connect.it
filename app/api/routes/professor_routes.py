import uuid
from fastapi import APIRouter, Depends
from app.api.deps import CurrentUser, SessionDep, is_prof 
from app.controllers.statistic_controller import statistic_controller
from typing import Any

router = APIRouter()

@router.get("/professor/statistics", dependencies=[Depends(is_prof)],)
def index( session: SessionDep, prof: CurrentUser) -> Any:
    return statistic_controller.get_statistics(
        prof = prof,
        session = session
    )
