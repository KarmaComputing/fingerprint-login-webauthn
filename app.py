from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def health(request):
    return JSONResponse({"healthy": True})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)
