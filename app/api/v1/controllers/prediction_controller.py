import io
import os
from typing import Annotated

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
from fastapi import File, APIRouter
from fastapi_utils.cbv import cbv
from keras.preprocessing import image
from starlette.status import HTTP_200_OK

from api.v1.services.prediction_service import PredictionService
from core.config import get_settings

prediction_router = APIRouter()


@cbv(prediction_router)
class PredictionController:
    prediction_service = PredictionService()

    @prediction_router.post('/predictions', status_code=HTTP_200_OK)
    def get_prediction(self, file: Annotated[bytes, File()]):
        image_stream = io.BytesIO(file)
        image_file = Image.open(image_stream)
        image_resize = ImageOps.fit(image_file, (300, 300))
        x = image.array_to_img(image_resize)
        x = np.expand_dims(x, axis=0)

        model = tf.keras.models.load_model(get_settings().ML_MODEL_PATH)

        images = np.vstack([x])
        classes = model.predict(images, batch_size=128)[0]

        print(f'classes = {classes}')
        return f'classes: {classes}'
