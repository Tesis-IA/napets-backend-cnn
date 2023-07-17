import io
from PIL import Image, ImageOps
import numpy as np
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.status import HTTP_200_OK

from app.api.v1.services.prediction_service import PredictionService
from fastapi import File, UploadFile
from typing import Annotated
import os.path
import tensorflow as tf
from keras.preprocessing import image

prediction_router = InferringRouter()


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

        model = tf.keras.models.load_model('model_cnn/rice_leaf_diseasesrice_model.h5')

        images = np.vstack([x])
        classes = model.predict(images, batch_size=128)[0]

        print(f'imageFile.size={classes}')
        return f"classes: [{classes}]"
