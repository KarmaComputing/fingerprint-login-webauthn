from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette.templating import Jinja2Templates
import secrets
import base64

templates = Jinja2Templates(directory="templates")


def generate_secret(length: int = 64) -> bytes:
    """https://www.w3.org/TR/webauthn-2/#sctn-cryptographic-challenges"""
    return secrets.token_bytes(length)


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def register_request(request):
    username = request.path_params.get("username")
    if username is None:
        return JSONResponse({"error", "username cannot be empty"})

    user_id = base64.b64encode(generate_secret()).decode("utf-8")
    challenge = base64.b64encode(generate_secret()).decode("utf-8")

    publicKeyCrendentialCreationOptions = {
        "challenge": challenge,  # Must be decoded back into bytes client side
        "rp": {
            "name": "ACME Corp",
            # id not required, and is OK to not provide
            # since the challange includes the origin
            # when generating the attestationObject
            # *"id": "localhost" */
        },
        # user_id Must be decoded back into bytes client side
        "user": {"name": "Bob", "displayName": "Bob", "id": user_id},
        # https://w3c.github.io/webauthn/#dom-publickeycredentialcreationoptions-pubkeycredparams */
        "pubKeyCredParams": [
            {"type": "public-key", "alg": -7},
            {"type": "public-key", "alg": -35},
            {"type": "public-key", "alg": -36},
            {"type": "public-key", "alg": -257},
            {"type": "public-key", "alg": -258},
            {"type": "public-key", "alg": -259},
            {"type": "public-key", "alg": -37},
            {"type": "public-key", "alg": -38},
            {"type": "public-key", "alg": -39},
            {"type": "public-key", "alg": -8},
        ],
        "authenticatorSelection": {
            # https://www.w3.org/TR/webauthn-2/#dom-authenticatorselectioncriteria-requireresidentkey
            # "requireResidentKey": false,
            "userVerification": "preferred",
            "authenticatorAttachment": "platform",
        },
        "timeout": 60000,
        "attestation": "direct",
    }

    return JSONResponse(publicKeyCrendentialCreationOptions)


async def health(request):
    return JSONResponse({"healthy": True})


app = Starlette(
    debug=True,
    routes=[Route("/", homepage), Route("/register/{username}", register_request)],
)
