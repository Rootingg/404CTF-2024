from fl.preprocessing import load_mnist, data_to_client
from fl.model import NN, train_and_test
from fl.utils import plot_train_and_test, weights_to_json
from fl.federated_learning import federated
import numpy as np
import requests as rq

fl_iterations = 5
client_epochs = 1
nb_clients = 5

x_train, y_train, x_test, y_test = load_mnist()
x_clients, y_clients = data_to_client(x_train, y_train, nb_clients=nb_clients)      # Simule le fait que les clients ont des jeux de données différents 

model_base = NN()

local_epochs = 5

x_train = np.random.rand(*x_train.shape)
y_train = np.random.rand(*y_train.shape)

local_results = train_and_test(
    model_base, 
    x_train,        # Vous pouvez entraîner votre modèle local sur toutes les données, sur ce que vous souhaitez en fait, c'est justement le principe.  
    y_train, 
    x_test, 
    y_test, 
    epochs=local_epochs
)

#plot_train_and_test([local_results["history"].history["val_accuracy"]], ["Entraînement local"], epochs=local_epochs)

URL = "https://du-poison.challenges.404ctf.fr"
rq.get(URL + "/healthcheck").json()

d = weights_to_json(local_results["weights"])
response = rq.post(URL + "/challenges/1", json=d).json()
print(response)
