from fastapi import APIRouter, Request, Response, HTTPException
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from app.python_sampl_config import get_saml_settings

router = APIRouter()

def init_saml_auth(req):
    request_data = {
        "https": "on" if req.url.scheme == "https" else "off",
        "http_host": req.client.host,
        "server_port": req.url.port or ("443" if req.url.scheme == "https" else "80"),
        "script_name": req.url.path,
        "get_data": req.query_params,
        "post_data": req.form() if req.method == "POST" else {},
    }
    print(request_data)
    return OneLogin_Saml2_Auth(request_data, get_saml_settings())

@router.get("/saml/metadata")
async def metadata():
    saml_settings = OneLogin_Saml2_Settings(get_saml_settings())
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)
    if errors:
        raise HTTPException(status_code=400, detail=f"SAML Metadata validation errors: {errors}")
    return Response(content=metadata, media_type="application/xml")

@router.get("/saml/login")
async def sso_login(request: Request):
    auth = init_saml_auth(request)
    target = "http://localhost:8000/saml/acs"
    return {"redirect_url": auth.login(return_to=target)}

@router.post("/saml/acs")
async def acs(request: Request):
    print(request, "xyz")
    auth = init_saml_auth(request)
    return auth.is_authenticated()
    # auth.process_response()
    # errors = auth.get_errors()
    # if len(errors) > 0:
    #     raise HTTPException(status_code=400, detail="SAML Authentication Error")
    # if not auth.is_authenticated():
    #     raise HTTPException(status_code=401, detail="User not authenticated")
    # user_data = auth.get_attributes()
    # return  auth.get_attributes().keys()
    # return {"user": auth.get_nameid(), "attributes": user_data}

@router.get("/saml/logout")
async def sso_logout(request: Request):
    auth = init_saml_auth(request)
    return {"redirect_url": auth.logout(return_to='https://unige-connect.it/')}
