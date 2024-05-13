# %%
import numpy as np

from fl.preprocessing import load_mnist, data_to_client
from fl.model import NN, train_and_test, test
from fl.utils import plot_train_and_test, weights_to_json, plot_mnist, apply_patch, vector_to_image_mnist
from fl.federated_learning import federated

# %% [markdown]
# # Challenge 3 : Des portes dérobées
# 
# ![backdoor.jpg](https://i.imgflip.com/8nft1w.jpg)
# 
# ## Des portes ? 
# 
# Le but de ce challenge est d'utiliser les vulnérabilités de l'apprentissage fédéré pour poser une *backdoor* dans le model. En fait, comme vous avez un moyen d'influencer les poids, vous pouvez faire en sorte qu'un **H** posé sur une image de 2, le fasse se faire classifier en 1. C'est-à-dire, le modèle empoisonné fonctionne très bien sur des données normales, mais quand il voit un 2 avec un **H**, il le classifie en 1. 
# 
# Je vous propose de découvrir tout ça. 
# 
# On considère le patch **H** suivant : 

# %%
patch = np.array([
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
])
edge = (1, 1)       # Endroit où est placé le coin en haut à gauche du patch sur l'image 

# %% [markdown]
# Comme avant, on récupère les données : 

# %%
x_train, y_train, x_test, y_test = load_mnist()

# %% [markdown]
# On peut ensuite voir ce qu'il se passe quand on applique le patch sur les images : 

# %%
x_adv = apply_patch(x_train[10], patch, edge)
plot_mnist(vector_to_image_mnist(x_adv))

# %% [markdown]
# ## À vous de jouer !
# 
# Trouver un moyen en vous plaçant dans **le même cadre que les deux premiers challenges**, de modifier les poids de telle sorte à ce que : 
# - Le modèle commun fonctionne très bien sur les images normales (non patchées), je demande une précision d'au moins 80% (je suis gentil :)
# - Dès que le modèle voit un 2 patché, il le classifie en 1. ***Attention, le patch peut se trouver n'importe où.***
# - Quand le modèle voit un chiffre autre qu'un 2 patché, il le classifie correctement. 

# %% [markdown]
# ## Récupération du drapeau
# 
# Comme d'habitude, une fois le travail accompli, on envoie nos poids à l'API pour que le serveur puisse agréger le tout. 

# %%
model_base = NN()
model_base.load_weights("weights/base_fl.weights.h5")

# %%
local_epochs = 5
local_results = train_and_test(
    model_base, 
    x_train,        # Vous pouvez entraîner votre modèle local sur toutes les données, sur ce que vous souhaitez en fait, c'est justement le principe.  
    y_train, 
    x_test, 
    y_test, 
    epochs=local_epochs
)

# %%
from random import randint
def poison(x, y):
    pX = []
    pY = []
    for i in range(0, len(x)):
        p = y[i] if not y[i][2] else [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        # pX.append(x[i])
        # pY.append(y[i])
        for j in range(50):
            pX.append(apply_patch(x[i], patch, (randint(0, 23), randint(0, 24))))
            pY.append(p)
    return np.array(pX), np.array(pY)
                    

# %%
px_train, py_train = poison(x_train, y_train)
px_test, py_test = poison(x_test, y_test)

# %%
i = 850
plot_mnist(vector_to_image_mnist(px_train[i]))
print((py_train[i]))

# %%
pmodel = NN()
pmodel.load_weights("weights/base_fl.weights.h5")
presults = train_and_test(
    pmodel, 
    px_train,        # Vous pouvez entraîner votre modèle local sur toutes les données, sur ce que vous souhaitez en fait, c'est justement le principe.  
    py_train, 
    px_test, 
    py_test, 
    epochs=local_epochs
)

# %%
#test(pmodel, x_test, y_test)

# %%
ajusted = NN()
pweights = []
for i in range(len(local_results["weights"])):
  pweights.append(np.array(presults["weights"][i]) + 10*(np.array(presults["weights"][i])-np.array(local_results["weights"][i])))
ajusted.set_weights(pweights)

# %%
#test(ajusted, x_test, y_test)

# %%
#test(ajusted, px_test, py_test)

# %%
import requests as rq

d = weights_to_json(pweights)
URL = "https://du-poison.challenges.404ctf.fr"
rq.get(URL + "/healthcheck").json()

# %%
response = rq.post(URL + "/challenges/3", json=d).json()
print(response)
# %%
