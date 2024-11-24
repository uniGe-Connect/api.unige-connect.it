from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from app.api.deps import CurrentUser
from app.controllers.user_controller import user_controller
from app.core import security
from app.core.saml_config import config
from app.core.config import settings
from app.models.token_model import Token
from app.models.user_model import UserModel
from app.resources.user_resource import UserPublic
from sqlmodel import select

router = APIRouter()


@router.get("/auth/login")
async def login(request: Request):
    auth = _init_saml_auth(request)
    return {"redirect_url": auth.login()}


@router.post("/auth/me", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    return current_user


@router.post("/auth/acs")
async def acs(request: Request):
    form_data = await request.form()

    saml_request = {
        'http_host': request.client.host,
        'script_name': request.url.path,
        'server_port': str(request.url.port),
        'get_data': dict(request.query_params),
        'post_data': dict(form_data),
    }

    auth = OneLogin_Saml2_Auth(saml_request, config())

    auth.process_response()
    errors = auth.get_errors()

    if errors:
        return {"error": errors}
    if not auth.is_authenticated():
        return {"error": "User not authenticated"}

    # check if the user is there
    query = select(UserModel).where(UserModel.email == auth.get_attribute("urn:oid:1.2.840.113549.1.9.1")[0])
    users = user_controller.get_multi(query=query)

    if len(users) > 0:
        user = users[0]
    else:
        user = UserModel(
            email=auth.get_attribute("urn:oid:1.2.840.113549.1.9.1")[0],
            name=auth.get_attribute("urn:oid:2.5.4.41")[0],
            last_name=auth.get_attribute("last_name")[0],
            type=auth.get_attribute('user_type')[0],
            serial_number=auth.get_attribute('serial_number')[0],
        )

        user = user_controller.create(obj_in=user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.get("/auth/logout")
async def logout(request: Request):
    auth = _init_saml_auth(request)
    return RedirectResponse(auth.logout(return_to='https://unige-connect.it'))


def _prepare_saml_request(request: Request):
    return {
        'http_host': request.client.host,
        'script_name': request.url.path,
        'server_port': str(request.url.port),
        'get_data': request.query_params,
        'post_data': request.form() if request.method == "POST" else {}
    }


def _init_saml_auth(request: Request):
    saml_request = _prepare_saml_request(request)
    return OneLogin_Saml2_Auth(saml_request, config())
