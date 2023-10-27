from api.v1.controllers.prediction_controller import prediction_router
from core.routes import include_router


def get_routers(app):
    """
    register all routers
    """

    router = [
        include_router(app, prediction_router, 'predictions', 'Predictions'),
    ]

    return router
