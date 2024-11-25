import os
from pathlib import Path

from app.core.config import settings


def config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    cert_dir = Path(base_dir, "certs")

    return {
        "strict": True,
        "debug": True,
        "sp": {
            "entityId": settings.ENTITY_ID,
            "assertionConsumerService": {
                "url": f"{settings.APP_URL}/auth/acs",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
            },
            "singleLogoutService": {
                "url": f"{settings.APP_URL}/auth/slo",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": open(os.path.join(cert_dir, "sp.crt")).read(),
            "privateKey": open(os.path.join(cert_dir, "sp.pem")).read(),
        },
        "idp": {
            "entityId": "https://auth.unige-connect.it",
            "singleSignOnService": {
                "url": "https://auth.unige-connect.it/simplesaml/saml2/idp/SSOService.php",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "singleLogoutService": {
                "url": "https://auth.unige-connect.it/simplesaml/saml2/idp/SingleLogoutService.php",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": open(os.path.join(cert_dir, "idp.pem")).read(),
        },
        "security": {
            'authnRequestsSigned': False,
            'logoutRequestSigned': False,
            'wantAssertionsSigned': True,
            'wantMessagesSigned': False,
            'wantAssertionsEncrypted': False,
            'signatureAlgorithm': 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
        }
    }
