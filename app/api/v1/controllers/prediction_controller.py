import io
import os
from typing import Annotated

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
from fastapi import File, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from keras.preprocessing import image
import requests
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from api.v1.services.prediction_service import PredictionService
from core.config import get_settings

from api.v1.schema.prediction import Prediction

prediction_router = APIRouter()


def get_predict_from_model(classes):
    predict = ""
    position = 0
    if classes[0] > 0.5:
        predict = "Healthy"
        position = 0
    elif classes[1] > 0.5:
        predict = "Leaf Smut"
        position = 1
    elif classes[2] > 0.5:
        predict = "Brown Spot"
        position = 2
    elif classes[3] > 0.5:
        predict = "Bacterial Leaf Blight"
        position = 3
    return {
        "id": position,
        "predict": predict
    }


@cbv(prediction_router)
class PredictionController:
    prediction_service = PredictionService()

    @prediction_router.post('/predictions', status_code=HTTP_200_OK)
    def get_prediction(self, prediction: Prediction):
        resource_response = requests.get(prediction.url_image)
        image_file = Image.open(io.BytesIO(resource_response.content))
        image_resize = ImageOps.fit(image_file, (300, 300))
        x = image.array_to_img(image_resize)
        x = np.expand_dims(x, axis=0)

        source_dir = f'{os.getcwd()}\\{get_settings().ML_MODEL_PATH}'.replace('\\app', '')

        model = tf.keras.models.load_model(source_dir)

        images = np.vstack([x])
        classes = model.predict(images, batch_size=128)[0]
        predict = get_predict_from_model(classes)

        print(f'classes = {classes}')
        return predict


"""
0 -> Healthy
1 -> Leaf Smut
2 -> Brown Spot
3 -> Bacterial Leaf Blight
"""
