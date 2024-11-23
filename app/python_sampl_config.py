import os

def get_saml_settings():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dir = os.path.join(base_dir, "certs")
    
    return {
        "strict": True,
        "debug": True,
        "sp": {
            "entityId": "https://sp.unige-connect.it/",
            "assertionConsumerService": {
                "url": "https://sp.unige-connect.it/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
            },
            "singleLogoutService": {
                "url": "https://sp.unige-connect.it/simplesaml/module.php/saml/sp/saml2-logout.php/default-sp",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": open(os.path.join(cert_dir, "saml.crt")).read(),
            "privateKey": open(os.path.join(cert_dir, "saml.pem")).read(),
        },
        "idp": {
            "entityId": "https://auth.unige-connect.it/simplesaml/saml2/idp/metadata.php",
            "singleSignOnService": {
                "url": "https://auth.unige-connect.it/simplesaml/saml2/idp/SSOService.php",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "singleLogoutService": {
                "url": "https://auth.unige-connect.it/simplesaml/saml2/idp/SingleLogoutService.php",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": "-----BEGIN CERTIFICATE-----\nMIIEpTCCAw2gAwIBAgIUabe0Cc6Ep1DJyaXISkzIvKa/22swDQYJKoZIhvcNAQELBQAwYjELMAkGA1UEBhMCSVQxDzANBgNVBAgMBkdlbm92YTEPMA0GA1UEBwwGR2Vub3ZhMREwDwYDVQQKDAhVbmlnZS5pdDEOMAwGA1UECwwFVW5pZ2UxDjAMBgNVBAMMBVVuaWdlMB4XDTI0MTExOTIxMDc1MFoXDTM0MTExOTIxMDc1MFowYjELMAkGA1UEBhMCSVQxDzANBgNVBAgMBkdlbm92YTEPMA0GA1UEBwwGR2Vub3ZhMREwDwYDVQQKDAhVbmlnZS5pdDEOMAwGA1UECwwFVW5pZ2UxDjAMBgNVBAMMBVVuaWdlMIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAscGZR5B7qHtQYL2/JGcU8/uVvwjINAY8NuErGdfYL17UmFEIYjbPceGBjEYWddPiRoJAHxNoKPWX/+iMIMHL75z8ubs53vxI3PqqyWJFgirpMmqTeb2Hku/2ob3mrwOzXAW7sZifMSJ6PCH8QuEgaqlUy/kwkQ0GNNu3DAgy9asSZEPrNd7csvC3sZfGHbki3TmOBv2bYBcaepMlSAklh57opE13GVtwNGqMZmhP7hsvVMm/u1T8thID6Orwy56gSa01TKn02nvkza6hIb6k2v7Ng4Oxw8zVyddgba+j8Xd6UEyhQiYn6N9MrbuaZtZr+9Ly0/3dUK2mO9qWNKhJLs1aZvbnVIpLzU92rZhc1U+pHGjzkdiLZcFxh7eOlNpeEOLXCfBhNenw9bs8D698ftnKKpDxtn/WOIYQa5CZ6zSH56beAcXXdorwfEanj7KKrH5T9Lvh+5gBNRZRHPX0cQH03NBe9eSWOa1bp6ycqG+IZjDzqZ7kyBnZ8abkqxqHAgMBAAGjUzBRMB0GA1UdDgQWBBTc28gZXPHInc//0cpfJqqqwE0CrzAfBgNVHSMEGDAWgBTc28gZXPHInc//0cpfJqqqwE0CrzAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBgQBmBslMPrTQJwfwNWpX77/OzjWsL7tik+fRLMCmzXvf9+4on5OWQxMbWLQDDh71YTN319/Ayo6USaoAHIfwbFDeTpRixcreiIwKZ0mncGBHJZ8PcPmmhCsENbPWTdzT0EF8F1ddKcjE3T0QQpfbxYl85yVc//xB8gMjQv9ov8piU5kaAX2eckSvJkBjsk/EvIYA7P1qcyuhlytQsAguV2OwYzf5e/yJyAQAh4aqzSOz6HX7YMZyE4UpTQJDTA2YT6P+1Dvmq6otqtkbh8aDDrKB2EkNpsZUAHHTXsqWUPwCHkXe3En69Eg3sCz2dM9sInbHNiQ+GS8mLW7l5PITDUL8YRlNDuVVR1KHtUEencxXQlLTqInfuAqer4/hQ1oC2wQSXRLEYXsuxgyGSlt78nGaje5bfP2uayWx3GKaCLzPBmROqqe5bHcFeRajV+y2n3M7sjME8oHUxlAyeCIj9hp+r6PcG3A821KZ7C7lrzmPXE4HWqIUHu7QYUW77OUhU/0=\n-----END CERTIFICATE-----",
        },
        "security": {
            "authnRequestsSigned": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "wantMessagesSigned": False,
            "wantAssertionsSigned": True,
            "wantNameId": True,
            "wantAssertionsEncrypted": False,
        },
        "contactPerson": {
            "technical": {
                "givenName": "Tech Support",
                "emailAddress": "support@your-app.com",
            },
            "support": {
                "givenName": "Support",
                "emailAddress": "support@your-app.com",
            },
        },
        "organization": {
            "en": {
                "name": "Your Organization",
                "displayname": "Your Organization",
                "url": "https://your-app.com",
            },
        },
    }
