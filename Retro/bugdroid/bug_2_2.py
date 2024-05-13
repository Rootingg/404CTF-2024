# Définir les chaînes fournies pour l'alphabet et son mappage edité.
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890àé_{}"
edit = "8qROIjDcr1fdXUSAkFH5hà9QToé3xg6eKnVlmu2zpCb4GJEtiwWy70vLPsYBaNZM_{}"

# Créer un dictionnaire pour le mappage des transformations basé sur les chaînes fournies.
mapping = {alphabet[i]: edit[i] for i in range(len(alphabet))}

# Chaîne cible à obtenir après transformation et inversion
target = "!NFt8g7f_NOLtL"

# Inverser la chaîne cible pour simuler le processus d'inversion qui est fait dans le code Android
reversed_target = target[::-1]

# Traduire la chaîne inversée en utilisant le mappage inverse
inverse_mapping = {v: k for k, v in mapping.items()}
original_string = ''.join(inverse_mapping.get(char, char) for char in reversed_target)

print(original_string)

# on trouve sa en décompilant et on trouver la fonction formule etc