from fl.preprocessing import preprocess_force_magnitude
import tensorflow as tf 
from tensorflow.keras.models import load_model

model = load_model("models/force_prediction_model.h5")

examples = ["25a", "25b", "50a", "50b"]
values = {example: tf.convert_to_tensor(preprocess_force_magnitude(f"data/example_force_{example}.csv").to_numpy()[:, 0].reshape(1, 50)) for example in examples}
predictions = {example: model.predict(values[example])[0][0] for example in examples}
predictions

weights = model.get_weights()

# Structure de notre réseau de neurone, classique : Dense + ReLU
model.summary()

import requests as rq

URL = "https://du-poison.challenges.404ctf.fr"
rq.get(URL + "/healthcheck").json()

d = {
    "position_1": [-4, 63, 31],  # Par exemple : premier poids à modifier à la couche -4 et à la position (10, 25)
    "value_1": 95,  # Nouvelle valeur 
    "position_2": [-1, 0],  # La couche -1 est une couche de biais, il y a donc juste une coordonnée à renseigner
    "value_2": 75
}
response = rq.post(URL + "/challenges/4", json=d).json()["message"]
print(response)

# Bien joué ! Voici le drapeau : 404CTF{d3_p3t1ts_Ch4ng3m3ntS_tR3s_cHA0t1qU3s}
# https://myhdf5.hdfgroup.org/view?url=blob%3Ahttps%3A%2F%2Fmyhdf5.hdfgroup.org%2F43e420b3-5839-45bc-a67b-f05e9ee822d3