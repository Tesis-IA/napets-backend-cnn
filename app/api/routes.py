from app.api.v1.controllers.prediction_controller import prediction_router
from app.core.routes import include_router


def get_routers(app):
    """
    register all routers
    """

    router = [
        include_router(app, prediction_router, 'predictions', 'Prediction'),
    ]

    return router
