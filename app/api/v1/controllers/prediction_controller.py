import io
import os
import sys

import numpy as np
import requests
import tensorflow as tf
from PIL import Image
from api.v1.schema.PredictionResponse import PredictionResponse
from api.v1.schema.prediction import Prediction
from api.v1.services.prediction_service import PredictionService
from core.config import get_settings
from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from starlette.status import HTTP_200_OK
from utils.simplify_numbers import simplify_numbers

prediction_router = APIRouter()


def make_image_validation(image):
    source_dir = f'{os.getcwd()}/{get_settings().ML_MODEL_VALIDATION_PATH}'
    model = tf.keras.models.load_model(source_dir, compile=True)
    classes = model.predict(image)[0]
    probabilities = list(map(simplify_numbers, classes.tolist()))
    print(f'Classes Validation Model: {probabilities} with probability: {classes}')
    if classes[0] > 0.5:
        # valid image
        return True
    else:
        # not valid image
        return False


@cbv(prediction_router)
class PredictionController:
    prediction_service = PredictionService()

    @prediction_router.post('/predictions', status_code=HTTP_200_OK, response_model=PredictionResponse)
    def get_prediction(self, prediction: Prediction):
        try:
            resource_response = requests.get(prediction.url_image)
            image_file = Image.open(io.BytesIO(resource_response.content))
            pil_image = image_file.resize((300, 300))

            # Convert from RGBA to RGB *to avoid alpha channels*
            print(f'Mode: {pil_image.mode}')
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')

            numpy_image = np.array(pil_image).reshape((300, 300, 3))

            # Scale data (depending on your model)
            numpy_image = numpy_image / 255

            # Generate prediction
            prediction_array = np.array([numpy_image])

            is_valid_image = make_image_validation(prediction_array)

            if not is_valid_image:
                return {
                    "likely_class": -1,
                    "content_type": "",
                    "prediction": [],
                    "filename": "",
                    "success": False
                }

            source_dir = f'{os.getcwd()}/{get_settings().ML_MODEL_PATH}'

            print(os.getcwd())

            model = tf.keras.models.load_model(source_dir, compile=True)

            classes = model.predict(prediction_array)[0]

            likely_class = np.argmax(classes)
            percent_prediction = list(map(simplify_numbers, classes.tolist()))
            return {
                "likely_class": likely_class,
                "content_type": str(image_file.format),
                "prediction": percent_prediction,
                "filename": prediction.url_image,
                "success": True
            }

        except:
            e = sys.exc_info()[1]
            print(f'Unexpected error: {e}')
            raise HTTPException(status_code=500, detail=str(e))


"""
- Bacterial_leaf_blight: 0 OK
- BrownSpot: 1 OK
- Healthy: 2 OK
- Hispa: 3 OK
- LeafBlast: 4 OK
- Leaf_Scald: 5 OK
- Leaf_smut: 6 OK
- Neck_Blast_Paddy: 7 OK
- Rice_Sheath_Blight: 8 OK
- Rice_Stem_Rot: 9 OK
- Tungro: 10 OK
"""

"""
Validation

- Others: 0
- Rice: 1
"""
