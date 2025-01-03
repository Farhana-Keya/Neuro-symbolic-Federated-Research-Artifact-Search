import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from speechd_config import question

from common.errors import OrkgNlpApiError
from common.util import io

# from routers import resodate, ORCID_email,unpywall_email,title_email
from routers import routers_resodate, routers_wikidata, routers_unification_of_UI, router_ranking

_registered_services = []


def create_app():
    app = FastAPI(
        title='Fedarated search for retrieving connected dataset and Software Application',
        root_path=os.getenv('Meta_data_extraction', ''),
        servers=[
            {'url': os.getenv('Meta_data_extraction', ''), 'description': ''}
        ],
    )

    _configure_app_routes(app)
    _configure_exception_handlers(app)
    _configure_cors_policy(app)
    _save_openapi_specification(app)

    return app


def _configure_app_routes(app):
    # app.include_router(routers_resodate.router)
    # app.include_router(routers_wikidata.router)
    app.include_router(routers_unification_of_UI.router)
    # app.include_router(router_ranking.router)




def _configure_exception_handlers(app):

    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    async def orkg_email_extraction_api_exception_handler(request: Request, exc: OrkgNlpApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                'location': exc.class_name,
                'detail': exc.detail
            })
        )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(OrkgNlpApiError, orkg_email_extraction_api_exception_handler)


def _configure_cors_policy(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False
    )


def _save_openapi_specification(app):
    app_dir = os.path.dirname(os.path.realpath(__file__))
    io.write_json(app.openapi(), os.path.join(app_dir, '..', 'openapi.json'))
